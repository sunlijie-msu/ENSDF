#!/usr/bin/env python3
"""
ENSDF-Agent Hook: Block git restore/checkout for error recovery (cross-platform)
-----------------------------------------------------------------------
Python port of block-git-revert.ps1 for Linux/macOS compatibility.

Enforces the Error Recovery Protocol in ENSDF-Agent.agent.md:
  "Do NOT use 'git restore' or 'git checkout' on critical .ens files."

Hook event : PreToolUse
Blocks     : git restore/checkout that can affect .ens files
           : git restore/checkout that target non-temp paths
           : broad or ambiguous git restore/checkout forms
           : git -C <path> restore/checkout and similar option-prefixed forms
           : common wrapped shell forms such as cmd /c, powershell -Command,
             bash -c, and pwsh -Command when they invoke git restore/checkout
Allows     : explicit temp script/code paths that do not touch .ens files
           : unrelated terminal commands that merely mention those words as text

Output     : JSON with permissionDecision "deny" - blocks the single tool
             call without stopping the agent session.
-----------------------------------------------------------------------
"""

import json
import re
import sys


def load_input():
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


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
    return normalized.strip()


def is_ens_path_spec(token):
    normalized = normalize_path_token(token)
    if not normalized:
        return False
    return bool(re.search(r'(?i)(^|/)[^/]*\.ens$', normalized))


def is_temp_path_spec(token):
    normalized = normalize_path_token(token)
    if not normalized:
        return False
    if normalized in ('.', '*'):
        return False
    return bool(re.search(r'(?i)(^|/)(temp|tmp)(/|$)', normalized))


def is_strong_temp_file_path(token):
    normalized = normalize_path_token(token)
    if not is_temp_path_spec(normalized):
        return False
    return bool(re.search(r'(?i)(^|/)[^/]+\.[A-Za-z0-9_*?-]+$', normalized))


def get_subcommand_option_value_count(subcommand, option_token):
    option = option_token.lower()
    if subcommand == 'restore':
        if option in ('-s', '--source', '-u', '--unified',
                      '--inter-hunk-context', '--pathspec-from-file'):
            return 1
    elif subcommand == 'checkout':
        if option in ('-b', '-B', '--orphan', '--conflict',
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
                skip_count = get_subcommand_option_value_count(subcommand, token)
                i += 1 + skip_count
                continue

            if subcommand == 'checkout' and not is_strong_temp_file_path(token):
                return {'path_specs': [], 'is_ambiguous': True}

        path_specs.append(token)
        i += 1

    return {'path_specs': path_specs, 'is_ambiguous': False}


def get_blocked_git_command(text, depth=0):
    if not text or not text.strip() or depth > 2:
        return None

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
        # Check for shell wrappers (powershell, pwsh, cmd, bash, sh, zsh)
        for i, token in enumerate(segment):
            raw_token = unquote_token(token)
            if re.match(r'(?i)^(powershell|pwsh|cmd|bash|sh|zsh)$', raw_token):
                for j in range(i + 1, len(segment) - 1):
                    wrapper_arg = unquote_token(segment[j])
                    if re.match(r'(?i)^(-command|-c|/c)$', wrapper_arg):
                        nested_text = unquote_token(segment[j + 1])
                        nested_match = get_blocked_git_command(nested_text, depth + 1)
                        if nested_match:
                            return nested_match
                        break

        # Look for git command
        for i, token in enumerate(segment):
            raw_token = unquote_token(token)
            if not re.search(r'(?i)(^|[\\/])git(?:\.exe)?$', raw_token):
                continue

            j = i + 1
            while j < len(segment):
                next_token = unquote_token(segment[j])
                if not next_token or not next_token.strip():
                    j += 1
                    continue

                if re.match(r'(?i)^(-c|-C|--config-env)$', next_token):
                    j += 2
                    continue

                if re.match(r'(?i)^(--git-dir|--work-tree|--namespace|--super-prefix)$', next_token):
                    j += 2
                    continue

                if next_token.startswith('-'):
                    j += 1
                    continue

                if re.match(r'(?i)^(checkout|restore)$', next_token):
                    subcommand = next_token.lower()
                    path_info = get_git_path_specs(segment, j, subcommand)
                    path_specs = path_info['path_specs']

                    if path_info['is_ambiguous']:
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

                    if any(not is_temp_path_spec(p) for p in path_specs):
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
    blocked_command = f"git {blocked_info['subcommand']}"
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
            'This command is blocked because at least one target path'
            ' is outside a temp folder.'
        ),
        'ambiguous': (
            'This command is blocked because `git checkout` without an explicit'
            ' temp file path is ambiguous and could switch branches or affect'
            ' critical files.'
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
        '  3. Fix errors using replace_string_in_file or multi_replace_string_in_file.',
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
        'continue': False,
        'stopReason': reason,
        'systemMessage': reason,
        'hookSpecificOutput': {
            'hookEventName': 'PreToolUse',
            'permissionDecision': 'deny',
            'permissionDecisionReason': reason,
        },
    }


def main():
    hook_input = load_input()
    if not hook_input:
        sys.exit(0)

    # Only act on terminal execution tools
    tool_name = hook_input.get('tool_name', '')
    is_terminal_tool = tool_name in (
        'execute/runInTerminal',
        'runInTerminal',
        'run_in_terminal',
    )
    if not is_terminal_tool:
        sys.exit(0)

    # Extract the command string
    tool_input = hook_input.get('tool_input') or {}
    command = tool_input.get('command', '')
    if not command:
        sys.exit(0)

    # Normalize: collapse whitespace
    cmd = re.sub(r'[\r\n]+', ' ', command)
    cmd = re.sub(r'\s+', ' ', cmd).strip()

    blocked_info = get_blocked_git_command(cmd)
    if not blocked_info:
        sys.exit(0)

    output = build_denial_output(blocked_info, cmd)
    sys.stdout.write(json.dumps(output))
    sys.exit(0)


if __name__ == '__main__':
    main()
