#!/usr/bin/env python3
"""
ENSDF Workspace Hook: Block file creation in protected directories (cross-platform)
-----------------------------------------------------------------------
Cross-platform Copilot command hook.

Hook event : PreToolUse
Blocks     : create_file / edit/createFile and apply_patch add-file operations when
             the target resolves to:
             (1) The workspace root directory
             (2) Any path under A<N>/ (A34, A35, A100, ... any mass number)
             (3) Any path under XUNDL/
Allows     : File creation under .github/ (e.g. .github/temp/)
             and any other non-protected subdirectory

Output     : JSON with permissionDecision "deny" — blocks the single tool
             call without stopping the agent session.
-----------------------------------------------------------------------
"""

import json
import os
import re
import sys
from urllib.parse import urlsplit
from urllib.request import url2pathname


CREATE_TOOL_NAMES = {
    "create",
    "create_file",
    "createFile",
    "writeFile",
    "edit/createFile",
    "functions.create_file",
    "vscode.createFile",
    "Write",
    "write",
}
DIRECTORY_TOOL_NAMES = {
    "create_directory",
    "createDirectory",
    "edit/createDirectory",
    "functions.create_directory",
    "vscode.createDirectory",
}
PATCH_TOOL_NAMES = {"apply_patch", "applyPatch", "edit/applyPatch", "functions.apply_patch"}
TERMINAL_TOOL_NAMES = {
    "run_in_terminal",
    "runInTerminal",
    "execute/runInTerminal",
    "functions.run_in_terminal",
    "Bash",
    "bash",
    "PowerShell",
    "powershell",
}
WRITE_COMMANDS = {
    "new-item",
    "ni",
    "set-content",
    "sc",
    "add-content",
    "ac",
    "out-file",
    "of",
    "mkdir",
    "md",
    "new-item -itemtype directory",
    "copy-item",
    "cp",
    "move-item",
    "mv",
    "tee-object",
    "tee",
}
PATH_OPTIONS = {
    "-path",
    "-literalpath",
    "-destination",
    "-target",
    "-filepath",
    "-name",
}
OPTIONS_WITH_VALUES = PATH_OPTIONS | {
    "-itemtype",
    "-value",
}


def load_input():
    try:
        raw = sys.stdin.buffer.read()
    except AttributeError:
        raw = sys.stdin.read().encode("utf-8", "replace")
    if not raw:
        return {}, "Hook input was empty; file creation was blocked."
    for encoding in ("utf-8-sig", "utf-8"):
        try:
            payload = json.loads(raw.decode(encoding))
            if not isinstance(payload, dict):
                return {}, "Hook input was not a JSON object; file creation was blocked."
            return payload, ""
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
    return {}, "Hook input was not valid UTF-8 JSON; file creation was blocked."


def emit_denial(reason):
    output = {
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }
    print(json.dumps(output))


def working_directory(hook_input):
    cwd = hook_input.get("cwd")
    if isinstance(cwd, str) and cwd.strip():
        return os.path.realpath(os.path.normpath(cwd))
    return os.path.realpath(os.getcwd())


def workspace_root():
    return os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def unquote_token(token):
    if len(token) >= 2 and token[0] == token[-1] and token[0] in ('"', "'"):
        return token[1:-1]
    return token


def resolve_path(file_path, cwd):
    if file_path.lower().startswith("file:"):
        parsed = urlsplit(file_path)
        if parsed.query or parsed.fragment:
            raise ValueError("File URI must not contain a query or fragment.")
        uri_path = parsed.path
        if parsed.netloc and parsed.netloc.lower() != "localhost":
            uri_path = "//" + parsed.netloc + uri_path
        file_path = url2pathname(uri_path)
    if not os.path.isabs(file_path):
        file_path = os.path.join(cwd, file_path)
    return os.path.realpath(os.path.normpath(file_path))


def classify_path(file_path, workspace_root, cwd):
    """Return (violation_kind, matched_directory, absolute_path)."""
    absolute_path = resolve_path(file_path, cwd)
    root = os.path.realpath(os.path.normpath(workspace_root))
    parent_dir = os.path.dirname(absolute_path)

    try:
        relative_parent = os.path.relpath(parent_dir, root)
    except ValueError:
        return "", "", absolute_path

    if relative_parent == ".":
        return "root", "", absolute_path

    if relative_parent == os.pardir or relative_parent.startswith(os.pardir + os.sep):
        return "", "", absolute_path

    first_segment = relative_parent.replace("\\", "/").split("/")[0]
    if re.match(r"^A\d+$", first_segment, re.IGNORECASE):
        return "data", first_segment, absolute_path
    if first_segment.upper() == "XUNDL":
        return "data", first_segment, absolute_path
    return "", "", absolute_path


def extract_target_paths(hook_input):
    tool_name = hook_input.get("tool_name") or hook_input.get("toolName", "")
    tool_input = hook_input.get("tool_input") or hook_input.get("toolArgs") or {}
    if isinstance(tool_input, str) and tool_name in PATCH_TOOL_NAMES:
        tool_input = {"input": tool_input}
    if not isinstance(tool_input, dict):
        if tool_name in CREATE_TOOL_NAMES:
            return [("", "create_file")]
        if tool_name in DIRECTORY_TOOL_NAMES:
            return [("", "create_directory")]
        if tool_name in PATCH_TOOL_NAMES:
            return [("", "apply_patch")]
        return []

    if tool_name in CREATE_TOOL_NAMES or tool_name in DIRECTORY_TOOL_NAMES:
        for key in ("filePath", "file_path", "fileName", "file_name", "path", "uri"):
            value = tool_input.get(key)
            if isinstance(value, str) and value.strip():
                operation = "create_directory" if tool_name in DIRECTORY_TOOL_NAMES else "create_file"
                return [(value, operation)]
        operation = "create_directory" if tool_name in DIRECTORY_TOOL_NAMES else "create_file"
        return [("", operation)]

    if tool_name in PATCH_TOOL_NAMES:
        patch_text = tool_input.get("input") or tool_input.get("patch", "")
        if not isinstance(patch_text, str):
            return [("", "apply_patch")]
        paths = []
        for match in re.finditer(r"^\*\*\* Add File:\s*(.+?)\s*$", patch_text, re.MULTILINE):
            paths.append((match.group(1), "apply_patch add-file"))
        return paths

    if tool_name in TERMINAL_TOOL_NAMES:
        command = tool_input.get("command") or tool_input.get("input") or ""
        if not isinstance(command, str):
            return []
        return extract_terminal_targets(command)

    return []


# Stream-to-stream redirections (PowerShell 2>&1 / 1>&2, sh >&2) merge one
# I/O stream into another and never create files. Without special handling,
# "2>&1" tokenizes as "2>" + "1" and the bare "1" is misreported as a file
# redirection target in the workspace root (a false positive).
STREAM_REDIRECTION_RE = re.compile(
    r"(?<!\d)(?:\d+>\s*&\s*\d+|\*?>\s*&\s*\d+)(?!\d)"
)


def neutralize_stream_redirections(command):
    """Replace stream-to-stream redirections with spaces before tokenizing.

    Quoted occurrences are left untouched so literal text is preserved.
    """
    out = []
    i, n, quote = 0, len(command), None
    while i < n:
        ch = command[i]
        if quote:
            out.append(ch)
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch in ('"', "'"):
            quote = ch
            out.append(ch)
            i += 1
            continue
        m = STREAM_REDIRECTION_RE.match(command, i)
        if m:
            out.append(" " * (m.end() - m.start()))
            i = m.end()
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def extract_terminal_targets(command):
    """Return targets for common shell write commands and redirections.

    A missing target is represented by an empty path so the caller can deny
    ambiguous write operations instead of allowing them silently.
    """
    command = neutralize_stream_redirections(command)
    tokens = re.findall(r'"[^"]*"|\'[^\']*\'|&&|\|\||[|;&]|[^\s|;&]+', command)
    targets = []
    write_seen = False
    segment_has_target = False
    pending_option = None
    for raw_token in tokens:
        if raw_token in (";", "|", "||", "&", "&&"):
            if pending_option in ("path", "redirection") or (write_seen and not segment_has_target):
                operation = "terminal redirection" if pending_option == "redirection" else "terminal write"
                targets.append(("", operation))
            write_seen = False
            segment_has_target = False
            pending_option = None
            continue
        token = unquote_token(raw_token)
        if pending_option:
            if pending_option == "path":
                targets.append((token, "terminal write"))
                segment_has_target = True
            elif pending_option == "redirection":
                targets.append((token, "terminal redirection"))
                segment_has_target = True
            pending_option = None
            continue
        lower = token.lower()
        # Also match PowerShell's "*>" all-streams file redirect.
        redirection = re.match(r"^\d*(\*)?(>>|>)(.*)$", token)
        if redirection:
            target = redirection.group(3)
            # A target beginning with '&' is a stream descriptor (e.g. a quoted
            # literal "2>&1"), not a file path.
            if target.startswith("&"):
                continue
            if target:
                targets.append((target, "terminal redirection"))
                segment_has_target = True
            else:
                pending_option = "redirection"
            continue
        if lower in WRITE_COMMANDS or lower.startswith("new-item"):
            write_seen = True
            continue
        if write_seen and lower in OPTIONS_WITH_VALUES:
            pending_option = "path" if lower in PATH_OPTIONS else "value"
            continue
        if write_seen and not token.startswith("-") and lower not in ("file", "directory"):
            targets.append((token, "terminal write"))
            segment_has_target = True
    if pending_option in ("path", "redirection") or (write_seen and not segment_has_target):
        operation = "terminal redirection" if pending_option == "redirection" else "terminal write"
        targets.append(("", operation))
    return targets


def main():
    hook_input, parse_error = load_input()
    if parse_error:
        emit_denial(
            "BLOCKED by workspace security hook (block-root-file-creation).\n\n"
            + parse_error
        )
        sys.exit(0)
    tool_name = hook_input.get("tool_name") or hook_input.get("toolName")
    if not isinstance(tool_name, str) or not tool_name.strip():
        emit_denial(
            "BLOCKED by workspace security hook (block-root-file-creation).\n\n"
            "Hook input has no valid tool name; file creation cannot be verified safely."
        )
        sys.exit(0)

    target_paths = extract_target_paths(hook_input)
    if not target_paths:
        sys.exit(0)

    root = workspace_root()
    cwd = working_directory(hook_input)

    for file_path, operation in target_paths:
        if not file_path:
            emit_denial(
                "BLOCKED by workspace security hook (block-root-file-creation).\n\n"
                f"Reason: Ambiguous {operation} target; file creation cannot be verified safely.\n"
                "Use an explicit path under .github/temp/ for AI-generated files."
            )
            break
        violation, matched_dir, absolute_path = classify_path(file_path, root, cwd)
        if not violation:
            continue

        parent_dir = os.path.dirname(absolute_path)
        file_name = os.path.basename(absolute_path)
        if violation == "root":
            violation_detail = (
                f"Reason: Creating files directly in the workspace root is not allowed.\n"
                f"Operation: {operation}\n"
                f"Target: {file_name}\n"
                f"Root:   {root}"
            )
        else:
            violation_detail = (
                f"Reason: Creating files inside the protected {matched_dir}/ tree is not allowed.\n"
                f"Operation: {operation}\n"
                f"Target: {parent_dir}{os.sep}{file_name}\n"
                f"Policy: {matched_dir}/ contains evaluated nuclear data files (new/, old/, raw/, pdf/).\n"
                f"        These files must be managed through the ENSDF evaluation workflow,\n"
                f"        not created directly by AI tooling."
            )

        reason = (
            "BLOCKED by workspace security hook (block-root-file-creation).\n"
            "\n"
            + violation_detail
            + "\n\n"
            "Allowed location for AI-generated files:\n"
            "  .github/temp/   — temporary scripts and analysis files only"
        )
        emit_denial(reason)
        break

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        emit_denial(
            "BLOCKED by workspace security hook (block-root-file-creation).\n\n"
            f"Hook error; file creation could not be verified safely: {exc}"
        )
