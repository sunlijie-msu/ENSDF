#!/usr/bin/env python3
"""
ENSDF-Agent Hook: Block git restore/checkout for error recovery
-----------------------------------------------------------------------
Cross-platform Copilot command hook.

Enforces the Error Recovery Protocol in ENSDF-Agent.agent.md:
  "Do NOT use 'git restore' or 'git checkout' on critical .ens files."

Hook event : PreToolUse
Blocks     : git restore/checkout that can affect .ens files
           : git restore/checkout that target non-temp paths
           : broad or ambiguous git restore/checkout forms
           : unsafe git -C <path> restore/checkout forms
           : common wrapped shell forms such as cmd /c, powershell -Command,
             bash -c, and pwsh -Command when they invoke git restore/checkout
Allows     : explicit existing temp script/code files with unambiguous paths
           : unrelated terminal commands that merely mention those words as text

Output     : JSON with permissionDecision "deny" - blocks the single tool
             call without stopping the agent session.
-----------------------------------------------------------------------
"""

import base64
import binascii
import json
import os
import posixpath
import re
import sys


def load_input():
    try:
        raw = sys.stdin.buffer.read()
    except AttributeError:
        raw = sys.stdin.read().encode("utf-8", "replace")
    if not raw:
        raise ValueError("Hook input was empty.")
    for encoding in ("utf-8-sig", "utf-8"):
        try:
            payload = json.loads(raw.decode(encoding))
            if not isinstance(payload, dict):
                raise ValueError("Hook input was not a JSON object.")
            return payload
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
    raise ValueError("Hook input was not valid UTF-8 JSON.")


def unquote_token(token):
    if not token or len(token) < 2:
        return token
    if (token.startswith('"') and token.endswith('"')) or \
       (token.startswith("'") and token.endswith("'")):
        return token[1:-1]
    return token


def get_command_tokens(text):
    pattern = r'"[^"]*"|\'[^\']*\'|&&|\|\||[;|&]|[^\s;|&]+'
    return re.findall(pattern, text)


def normalize_path_token(token):
    normalized = unquote_token(token)
    if not normalized or not normalized.strip():
        return ''
    normalized = normalized.strip()
    if normalized.startswith('./'):
        normalized = normalized[2:]
    normalized = normalized.replace('\\', '/')
    return posixpath.normpath(normalized.strip())


def is_ens_path_spec(token):
    normalized = normalize_path_token(token)
    if not normalized:
        return False
    return bool(re.search(r'(?i)(^|/)[^/]*\.ens$', normalized))


CODE_EXTENSIONS = {
    '.py', '.pyi', '.js', '.mjs', '.cjs', '.jsx', '.ts', '.tsx',
    '.sh', '.bash', '.ps1', '.psm1', '.bat', '.cmd', '.c', '.h',
    '.cc', '.cpp', '.cxx', '.hpp', '.go', '.rs', '.java', '.sql',
}


def has_dynamic_path_syntax(path):
    return any(char in path for char in '*?[]$%`~\n\r') or path.startswith(':')


def resolve_path(path, cwd, follow_links=True):
    if not path or has_dynamic_path_syntax(path):
        return None
    drive, tail = os.path.splitdrive(path)
    if drive and not os.path.isabs(path):
        return None
    if os.name == 'nt' and os.path.isabs(path) and not drive:
        return None
    if ':' in tail:
        return None
    if not os.path.isabs(path):
        path = os.path.join(cwd, path)
    path = os.path.abspath(path)
    return os.path.realpath(path) if follow_links else path


def is_safe_temp_file(path, cwd):
    lexical = resolve_path(path, cwd, follow_links=False)
    resolved = resolve_path(path, cwd)
    if not lexical or not resolved:
        return False
    for candidate in (lexical, resolved):
        parts = os.path.normcase(candidate).replace('\\', '/').split('/')
        if (not any(part.lower() in ('temp', 'tmp') for part in parts[:-1])
                or os.path.splitext(candidate)[1].lower() not in CODE_EXTENSIONS):
            return False
    return os.path.isfile(resolved)


def get_subcommand_option_value_count(subcommand, option_token):
    if subcommand == 'restore':
        if option_token in ('-s', '--source', '-u', '--unified',
                            '--inter-hunk-context', '--pathspec-from-file'):
            return 1
    elif subcommand == 'checkout':
        if option_token in ('-b', '-B', '--orphan', '--conflict',
                            '--pathspec-from-file'):
            return 1
    return 0


def get_git_path_specs(segment, subcommand_index, subcommand):
    path_specs = []
    saw_double_dash = False
    i = subcommand_index + 1
    while i < len(segment):
        token = unquote_token(segment[i])
        if not token or not token.strip():
            i += 1
            continue

        if token == '--':
            saw_double_dash = True
            i += 1
            continue

        if not saw_double_dash:
            if token.startswith('-'):
                if token == '--pathspec-from-file' or token.startswith('--pathspec-from-file='):
                    return {'path_specs': [], 'is_ambiguous': True}
                if subcommand == 'checkout' and token in ('-b', '-B', '--orphan'):
                    return {'path_specs': [], 'is_ambiguous': True}
                skip_count = get_subcommand_option_value_count(subcommand, token)
                known_flag = token in (
                    '-p', '--patch', '-W', '--worktree', '-S', '--staged',
                    '-q', '--quiet', '--progress', '--no-progress', '--ours',
                    '--theirs', '--merge', '--ignore-unmerged', '--overlay',
                    '--no-overlay', '-f', '--force', '--ignore-skip-worktree-bits',
                )
                known_value = (token.startswith('--source=') or
                               token.startswith('--conflict=') or
                               token.startswith('--unified=') or
                               token.startswith('--inter-hunk-context='))
                if not skip_count and not known_flag and not known_value:
                    return {'path_specs': [], 'is_ambiguous': True}
                if skip_count and i + skip_count >= len(segment):
                    return {'path_specs': [], 'is_ambiguous': True}
                i += 1 + skip_count
                continue

            if subcommand == 'checkout':
                return {'path_specs': [], 'is_ambiguous': True}

        path_specs.append(token)
        i += 1

    return {'path_specs': path_specs, 'is_ambiguous': False}


def get_blocked_git_command(text, cwd, depth=0, cwd_uncertain=False):
    if not text or not text.strip() or depth > 2:
        return None

    text = re.sub(r'[\r\n]+', ';', text)
    tokens = get_command_tokens(text)
    if not tokens:
        return None

    # Split into segments by shell separators
    segments = []
    current_segment = []
    for token in tokens:
        if token in (';', '|', '&', '&&', '||'):
            if current_segment:
                segments.append(current_segment)
                current_segment = []
        else:
            current_segment.append(token)
    if current_segment:
        segments.append(current_segment)

    for segment in segments:
        if segment and unquote_token(segment[0]).lower() in (
                'cd', 'chdir', 'set-location', 'push-location', 'pop-location'):
            cwd_uncertain = True
        # Check for shell wrappers (powershell, pwsh, cmd, bash, sh, zsh)
        for i, token in enumerate(segment):
            raw_token = unquote_token(token)
            executable = raw_token.replace('\\', '/').rsplit('/', 1)[-1].lower()
            if executable.endswith('.exe'):
                executable = executable[:-4]
            if executable in ('powershell', 'pwsh', 'cmd', 'bash', 'sh', 'zsh'):
                for j in range(i + 1, len(segment) - 1):
                    wrapper_arg = unquote_token(segment[j])
                    lower_arg = wrapper_arg.lower()
                    encoded = (
                        executable in ('powershell', 'pwsh')
                        and len(lower_arg) >= 2
                        and '-encodedcommand'.startswith(lower_arg)
                    )
                    is_command = (
                        lower_arg in ('-command', '-c', '/c')
                        or (executable in ('bash', 'sh', 'zsh')
                            and bool(re.fullmatch(r'-[a-z]*c[a-z]*', wrapper_arg)))
                    )
                    if encoded or is_command:
                        nested_text = unquote_token(segment[j + 1])
                        if encoded:
                            try:
                                nested_text = base64.b64decode(
                                    nested_text, validate=True).decode('utf-16-le')
                            except (binascii.Error, UnicodeDecodeError, ValueError):
                                return {
                                    'subcommand': '',
                                    'path_specs': [],
                                    'reason_code': 'opaque',
                                }
                        nested_match = get_blocked_git_command(
                            nested_text, cwd, depth + 1, cwd_uncertain)
                        if nested_match:
                            return nested_match
                        break

        # Look for git command
        for i, token in enumerate(segment):
            raw_token = unquote_token(token)
            if not re.search(r'(?i)(^|[\\/])git(?:\.exe)?$', raw_token):
                continue

            j = i + 1
            git_cwd = cwd
            git_context_uncertain = cwd_uncertain
            while j < len(segment):
                next_token = unquote_token(segment[j])
                if not next_token or not next_token.strip():
                    j += 1
                    continue

                if next_token == '-C' or next_token.startswith('-C'):
                    if next_token == '-C':
                        if j + 1 >= len(segment):
                            break
                        directory = unquote_token(segment[j + 1])
                        j += 2
                    else:
                        directory = next_token[2:]
                        j += 1
                    resolved = resolve_path(directory, git_cwd)
                    if resolved is None:
                        git_context_uncertain = True
                    else:
                        git_cwd = resolved
                    continue

                if next_token in ('-c', '--config-env'):
                    if j + 1 >= len(segment):
                        break
                    config = unquote_token(segment[j + 1]).lower()
                    if config.startswith(('core.worktree=', 'core.bare=')):
                        git_context_uncertain = True
                    j += 2
                    continue

                if next_token in ('--git-dir', '--work-tree', '--namespace', '--super-prefix'):
                    git_context_uncertain = True
                    j += 2
                    continue

                if next_token.startswith('-'):
                    if next_token not in ('--no-pager', '--paginate', '--no-optional-locks'):
                        git_context_uncertain = True
                    j += 1
                    continue

                if re.match(r'(?i)^(checkout|restore)$', next_token):
                    subcommand = next_token.lower()
                    path_info = get_git_path_specs(segment, j, subcommand)
                    path_specs = path_info['path_specs']

                    if path_info['is_ambiguous'] or git_context_uncertain:
                        return {
                            'subcommand': subcommand,
                            'path_specs': [],
                            'reason_code': 'ambiguous',
                        }

                    if not path_specs:
                        return {
                            'subcommand': subcommand,
                            'path_specs': [],
                            'reason_code': 'broad',
                        }

                    if any(is_ens_path_spec(p) for p in path_specs):
                        return {
                            'subcommand': subcommand,
                            'path_specs': path_specs,
                            'reason_code': 'ens',
                        }

                    if any(not is_safe_temp_file(p, git_cwd) for p in path_specs):
                        return {
                            'subcommand': subcommand,
                            'path_specs': path_specs,
                            'reason_code': 'non-temp',
                        }

                    break

                # Not checkout/restore — stop scanning this git command
                break

    return None


def build_denial_output(blocked_info, cmd):
    blocked_command = (f"git {blocked_info['subcommand']}"
                       if blocked_info['subcommand'] else 'PowerShell encoded command')
    command_excerpt = (cmd[:220] + '...') if len(cmd) > 220 else cmd

    if blocked_info['path_specs']:
        normalized = [normalize_path_token(p) for p in blocked_info['path_specs']]
        target_summary = 'Target paths:\n' + '\n'.join('  ' + p for p in normalized)
    else:
        target_summary = 'Target paths: none explicitly identified.'

    why_blocked_map = {
        'ens': (
            'This command is blocked because it targets one or more'
            ' .ens nuclear dataset files.'
        ),
        'non-temp': (
            'This command is blocked because at least one target is not an'
            ' explicit existing temp script/code file, or is a wildcard or directory.'
        ),
        'ambiguous': (
            'This command is blocked because its Git options, working directory,'
            ' or pathspec are ambiguous and could affect critical files.'
        ),
        'opaque': (
            'This command is blocked because its encoded PowerShell command'
            ' cannot be decoded for inspection.'
        ),
    }
    why_blocked = why_blocked_map.get(
        blocked_info['reason_code'],
        'This command is blocked because it does not explicitly limit itself'
        ' to temp script/code paths.',
    )

    reason = '\n'.join([
        'BLOCKED by ENSDF-Agent security hook.',
        '',
        f'Blocked command: {blocked_command}',
        'Command excerpt:',
        f'  {command_excerpt}',
        '',
        target_summary,
        '',
        why_blocked,
        '',
        'LESSON FOR THE AGENT:',
        '  .ens nuclear dataset files are super critical.',
        '  `git restore` and `git checkout` are forbidden for .ens editing work.',
        '  Temp scripts and code inside temp folders may be reverted, but only when',
        '  the command clearly targets temp paths and nothing else.',
        '',
        'This is an expected ENSDF-Agent policy denial, not a tool malfunction.',
        'Do not retry the same operation with alternate Git syntax, shell wrappers,',
        'aliases, or option variants.',
        '',
        'Required next actions:',
        '  1. If the target is a temp script/code file, use an explicit temp path only.',
        '  2. If the target is an .ens or other working file, identify the root cause'
        ' through analysis, not reversion.',
        '  3. Fix errors using edit tools, not reversion.',
        '  4. Validate .ens fixes with column_calibrate.py and ensdf_1line_ruler.py.',
        '  5. Use diff-aware edits so that users can review diffs in VS Code diff'
        ' viewer before accepting changes.',
        '',
        'If branch switching is explicitly requested by the user, use `git switch`,',
        'not `git checkout`.',
        '',
        'Rationale: Reversion bypasses the VS Code diff viewer, eliminating',
        'the mandatory human review layer that catches LLM formatting mistakes',
        'in nuclear data files.',
    ])

    return {
        'permissionDecision': 'deny',
        'permissionDecisionReason': reason,
    }


def main():
    try:
        hook_input = load_input()
    except ValueError as exc:
        sys.stdout.write(json.dumps({
            'permissionDecision': 'deny',
            'permissionDecisionReason': f'Cannot verify terminal command: {exc}',
        }))
        sys.exit(0)
    tool_name = hook_input.get('tool_name') or hook_input.get('toolName')
    if not isinstance(tool_name, str) or not tool_name.strip():
        sys.stdout.write(json.dumps({
            'permissionDecision': 'deny',
            'permissionDecisionReason': 'Cannot verify terminal command: hook input has no valid tool name.',
        }))
        sys.exit(0)

    # Only act on terminal execution tools
    is_terminal_tool = tool_name in (
        'execute/runInTerminal',
        'runInTerminal',
        'run_in_terminal',
        'Bash',
        'bash',
        'PowerShell',
        'powershell',
    )
    if not is_terminal_tool:
        sys.exit(0)

    # Extract the command string
    tool_input = hook_input.get('tool_input') or hook_input.get('toolArgs') or {}
    if not isinstance(tool_input, dict):
        sys.stdout.write(json.dumps({
            'permissionDecision': 'deny',
            'permissionDecisionReason': 'Cannot verify terminal command: tool arguments are not a JSON object.',
        }))
        sys.exit(0)
    command = tool_input.get('command', '')
    if not isinstance(command, str) or not command:
        sys.stdout.write(json.dumps({
            'permissionDecision': 'deny',
            'permissionDecisionReason': 'Cannot verify terminal command: command argument is missing.',
        }))
        sys.exit(0)

    cmd = re.sub(r'[\r\n]+', ';', command).strip()

    cwd = hook_input.get('cwd')
    cwd_uncertain = cwd is not None and (
        not isinstance(cwd, str) or not os.path.isabs(cwd))
    if cwd_uncertain or cwd is None:
        cwd = os.getcwd()
    blocked_info = get_blocked_git_command(
        cmd, os.path.realpath(cwd), cwd_uncertain=cwd_uncertain)
    if not blocked_info:
        sys.exit(0)

    output = build_denial_output(blocked_info, cmd)
    sys.stdout.write(json.dumps(output))
    sys.exit(0)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        sys.stdout.write(json.dumps({
            'permissionDecision': 'deny',
            'permissionDecisionReason': f'Cannot verify terminal command because the hook failed: {exc}',
        }))
