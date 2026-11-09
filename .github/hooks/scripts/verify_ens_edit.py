import json
import hashlib
import os
import re
import subprocess
import sys
import difflib
from urllib.parse import urlsplit
from urllib.request import url2pathname

MUTATING_RE = re.compile(r"--fix\b|>>?\s|Set-Content|Out-File|Add-Content|\.write_text\(|WriteAllText", re.IGNORECASE)
EDIT_TOOLS = {
    "replace_string_in_file", "multi_replace_string_in_file", "editFiles", "edit/editFiles",
    "create", "createFile", "create_file", "edit/createFile", "writeFile",
    "Edit", "edit", "Write", "write", "str_replace", "str_replace_editor",
}
PATCH_TOOLS = {"apply_patch", "applyPatch", "edit/applyPatch", "functions.apply_patch"}

# ENSDF-Agent Hook: Validate .ens files after edits
# --------------------------------------------------------
# PostToolUse event — runs two validation passes on any .ens file that was
# just created or edited by ENSDF-Agent:
#
#   PASS 1 (always): ASCII-only check — reports any non-ASCII character
#     found in the .ens file. Applies to ALL edits (data records AND comments).
#
#   PASS 2 (always when guard supplied an expectation): actual content must match
#     the PreToolUse predicted result, catching editor-side block collapse.
#
#   PASS 3 (data only): 80-column ruler validation via ensdf_1line_ruler.py.
#     Skipped for comment-only edits (per ENSDF-Agent.agent.md).
#
#   Token policy: only mutating calls (edits / apply_patch / create_file /
#     mutating terminal) consume the one-shot PreToolUse token. Read-only
#     calls exit early and never touch guard state — a read issues the token
#     that the immediately following edit depends on.
#
# Key features:
#   - Handles all VS Code file-editing tool input shapes
#   - Validates ALL .ens files touched by a single tool call (multi-file)
#   - Uses hook-provided cwd for robust script path resolution
#   - Returns Sacred Workflow guidance on failure; cannot undo completed tool calls
#
# Hook event : PostToolUse
# On failure : additionalContext with fix instructions
# On success : exit 0  (silent)


PATCH_HEADER_PREFIXES = (
    "*** Begin Patch",
    "*** End Patch",
    "*** Update File:",
    "*** Add File:",
    "*** Delete File:",
    "@@",
)


def emit(payload):
    data = json.dumps(payload).encode("utf-8")
    try:
        sys.stdout.buffer.write(data)
        sys.stdout.buffer.flush()
    except AttributeError:
        sys.stdout.write(json.dumps(payload))


def load_input():
    """Parse the hook payload from stdin as UTF-8 (never the console code page)."""
    try:
        raw = sys.stdin.buffer.read()
    except AttributeError:
        raw = sys.stdin.read().encode("utf-8", "replace")
    if not raw.strip():
        raise ValueError("Hook input was empty.")
    for enc in ("utf-8-sig", "utf-8"):
        try:
            payload = json.loads(raw.decode(enc))
            if not isinstance(payload, dict):
                raise ValueError("Hook input was not a JSON object.")
            return payload
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
    raise ValueError("Hook input was not valid UTF-8 JSON.")


def file_digest(path):
    with open(path, "r", encoding="utf-8", newline="") as fh:
        text = fh.read().replace("\r\n", "\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def workspace_root():
    return os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def pop_expected_hashes(paths, cwd, is_failure=False):
    """Return post-edit mismatches and whether any path changed, then consume tokens."""
    state_path = os.path.join(workspace_root(), ".github", "temp", "ens_guard", "state.json")
    try:
        with open(state_path, encoding="utf-8") as fh:
            state = json.load(fh)
    except FileNotFoundError:
        return [], True
    except (OSError, ValueError) as exc:
        raise ValueError(f"Cannot read ENSDF guard state {state_path}: {exc}") from exc
    if not isinstance(state, dict):
        raise ValueError(f"ENSDF guard state is not a JSON object: {state_path}")

    mismatches = []
    consumed = False
    changed = False
    untracked = False
    for path in paths:
        absolute = os.path.realpath(resolve_path(path, cwd))
        token = state.get(absolute)
        if not token:
            untracked = True
            continue
        consumed = True
        if isinstance(token, dict):
            before = token.get("before")
            expected = token.get("expected")
        else:
            before = token
            expected = token
        try:
            actual = file_digest(absolute)
        except OSError:
            actual = None
        if actual != before:
            changed = True
        unchanged_failure = is_failure and before is not None and actual == before
        if expected is None:
            if is_failure and before is not None and actual != before:
                mismatches.append((absolute, expected, actual))
        elif actual != expected and not unchanged_failure:
            mismatches.append((absolute, expected, actual))
        state.pop(absolute, None)

    if consumed:
        os.makedirs(os.path.dirname(state_path), exist_ok=True)
        with open(state_path, "w", encoding="utf-8") as fh:
            json.dump(state, fh)
    return mismatches, changed or untracked


def path_value(item):
    for field in ("filePath", "file_path", "fileName", "file_name", "path", "uri"):
        value = item.get(field)
        if isinstance(value, str) and value:
            return value
    return ""


def text_value(item, *fields):
    for field in fields:
        value = item.get(field)
        if isinstance(value, str):
            return value
    return None


def edit_entries(tool_input):
    """Return (path, old, new) entries for legacy and editFiles payloads."""
    entries = []
    direct_path = path_value(tool_input)
    direct_old = text_value(tool_input, "oldString", "old_string", "oldText", "old_text")
    direct_new = text_value(tool_input, "newString", "new_string", "newText", "new_text")
    if direct_path and direct_old is not None and direct_new is not None:
        entries.append((direct_path, direct_old, direct_new))

    for item in tool_input.get("replacements") or []:
        if not isinstance(item, dict):
            continue
        path = path_value(item) or direct_path
        old = text_value(item, "oldString", "old_string", "oldText", "old_text")
        new = text_value(item, "newString", "new_string", "newText", "new_text")
        if path and old is not None and new is not None:
            entries.append((path, old, new))

    for file_item in tool_input.get("files") or []:
        if not isinstance(file_item, dict):
            continue
        path = path_value(file_item)
        for item in file_item.get("edits") or file_item.get("operations") or []:
            if not isinstance(item, dict):
                continue
            old = text_value(item, "oldString", "old_string", "oldText", "old_text")
            new = text_value(item, "newString", "new_string", "newText", "new_text")
            if path and old is not None and new is not None:
                entries.append((path, old, new))

    for item in tool_input.get("edits") or tool_input.get("operations") or []:
        if not isinstance(item, dict):
            continue
        path = path_value(item) or direct_path
        old = text_value(item, "oldString", "old_string", "oldText", "old_text")
        new = text_value(item, "newString", "new_string", "newText", "new_text")
        if path and old is not None and new is not None:
            entries.append((path, old, new))
    return entries


def find_all_ens_paths(payload):
    """Collect all unique .ens file paths touched by this tool call.

    Handles four input shapes:
      - replace_string_in_file / create_file  → tool_input.filePath
    - multi_replace_string_in_file          → tool_input.replacements[*].filePath
    - editFiles / edit/editFiles            → tool_input.files[*].path
      - apply_patch                           → *** Update/Add File: <path> headers
      - TOOL_INPUT_FILE_PATH env var          → set by some integrations
    """
    paths = set()
    tool_input = payload.get("tool_input") or payload.get("toolArgs") or {}
    tool_name = payload.get("tool_name") or payload.get("toolName", "")
    if isinstance(tool_input, str) and tool_name in PATCH_TOOLS:
        tool_input = {"input": tool_input}
    if not isinstance(tool_input, dict):
        return []

    # Environment variable override (used by some Claude Code integrations)
    env_path = os.environ.get("TOOL_INPUT_FILE_PATH", "")
    if env_path and env_path.lower().endswith(".ens"):
        paths.add(env_path)

    # Direct and workspace-edit payloads
    for key in ("filePath", "file_path", "fileName", "file_name", "path", "uri"):
        value = tool_input.get(key)
        if isinstance(value, str) and value.lower().endswith(".ens"):
            paths.add(value)

    for file_item in tool_input.get("files") or []:
        if isinstance(file_item, dict):
            value = path_value(file_item)
            if value.lower().endswith(".ens"):
                paths.add(value)

    for item in tool_input.get("edits") or tool_input.get("operations") or []:
        if isinstance(item, dict):
            value = path_value(item)
            if isinstance(value, str) and value.lower().endswith(".ens"):
                paths.add(value)

    # multi_replace_string_in_file → tool_input.replacements[*].filePath
    replacements = tool_input.get("replacements")
    if isinstance(replacements, list):
        for item in replacements:
            if not isinstance(item, dict):
                continue
            for key in ("filePath", "file_path"):
                value = item.get(key)
                if isinstance(value, str) and value.lower().endswith(".ens"):
                    paths.add(value)

    # apply_patch → parse file paths from patch header lines
    patch_text = tool_input.get("input") or tool_input.get("patch") or tool_input.get("patchText")
    if isinstance(patch_text, str):
        for match in re.finditer(r"^\*\*\* (?:Update|Add|Delete) File: (.+)$", patch_text, re.MULTILINE):
            path = match.group(1).strip()
            if path.lower().endswith(".ens"):
                paths.add(path)

    # run_in_terminal / send_to_terminal → only when the command looks mutating
    # (avoids re-validating on every read-only script call)
    command_text = tool_input.get("command") or tool_input.get("input")
    if isinstance(command_text, str) and "--dry-run" not in command_text and MUTATING_RE.search(command_text):
        for match in re.finditer(r"[^\s\"']+\.ens", command_text, re.IGNORECASE):
            paths.add(match.group(0).strip("\"'"))

    return sorted(paths)


def extract_changed_lines_from_patch(patch_text):
    changed = []
    for line in patch_text.splitlines():
        if line.startswith(PATCH_HEADER_PREFIXES):
            continue
        if line.startswith("+") or line.startswith("-"):
            changed.append(line[1:])
    return changed


def extract_changed_lines_from_pair(old_text, new_text):
    changed = []
    diff = difflib.ndiff(old_text.splitlines(), new_text.splitlines())
    for line in diff:
        if line.startswith("? "):
            continue
        if line.startswith("+ ") or line.startswith("- "):
            changed.append(line[2:])
    return changed


def extract_all_changed_lines(payload):
    """Collect all changed ENSDF lines across all replacements in this tool call."""
    tool_name = payload.get("tool_name") or payload.get("toolName", "")
    tool_input = payload.get("tool_input") or payload.get("toolArgs") or {}

    if tool_name in PATCH_TOOLS:
        if isinstance(tool_input, str):
            patch_text = tool_input
        elif isinstance(tool_input, dict):
            patch_text = tool_input.get("input") or tool_input.get("patch") or tool_input.get("patchText", "")
        else:
            patch_text = ""
        if isinstance(patch_text, str):
            return extract_changed_lines_from_patch(patch_text)

    if not isinstance(tool_input, dict):
        return []

    changed = []

    for _, old_string, new_string in edit_entries(tool_input):
        changed.extend(extract_changed_lines_from_pair(old_string, new_string))

    content = tool_input.get("content")
    if isinstance(content, str):
        changed.extend(content.splitlines())

    return changed


def is_comment_record(line):
    return len(line) >= 7 and line[6] == "c"  # column 7 (0-indexed 6) is the comment flag


def is_noncomment_record(line):
    return len(line) >= 7 and line[6] != "c" and not line.isspace()


def comment_only_edit(payload):
    """Return True if ALL changed non-blank ENSDF records are comment (cL/cG) lines.

    Per ENSDF-Agent.agent.md: 'Skip ruler, column validation, and gamma ordering
    checks only if task is purely editing comments.'
    """
    changed_lines = extract_all_changed_lines(payload)
    record_lines = [line for line in changed_lines if len(line) >= 8]
    if not record_lines:
        return False
    return all(is_comment_record(line) for line in record_lines)


def find_ruler_script(payload):
    """Locate bundled ruler first, then the workspace copy."""
    plugin_root = os.environ.get("PLUGIN_ROOT", "")
    if plugin_root:
        candidate = os.path.join(plugin_root, "scripts", "ensdf_1line_ruler.py")
        if os.path.isfile(candidate):
            return candidate
    candidate = os.path.join(workspace_root(), ".github", "scripts", "ensdf_1line_ruler.py")
    if os.path.isfile(candidate):
        return candidate
    return candidate


def run_ruler(ruler_script, file_path):
    return subprocess.run(
        [sys.executable, ruler_script, "--file", file_path, "--show-only-wrong"],
        capture_output=True,
        text=True,
        check=False,
    )


def resolve_path(path, cwd):
    """Resolve a potentially relative path against a base directory."""
    if path.lower().startswith("file:"):
        parsed = urlsplit(path)
        if parsed.query or parsed.fragment:
            raise ValueError("File URI must not contain a query or fragment.")
        uri_path = parsed.path
        if parsed.netloc and parsed.netloc.lower() != "localhost":
            uri_path = "//" + parsed.netloc + uri_path
        path = url2pathname(uri_path)
    if os.path.isabs(path):
        return path
    return os.path.normpath(os.path.join(cwd, path))


def check_ascii_only(abs_path):
    """Return list of (line_number, non_ascii_chars) for any line containing non-ASCII."""
    violations = []
    try:
        with open(abs_path, "r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                non_ascii = [c for c in line if ord(c) > 127]
                if non_ascii:
                    violations.append((lineno, line.rstrip("\n"), non_ascii))
    except OSError as exc:
        raise OSError(f"Cannot read ENSDF file {abs_path}: {exc}") from exc
    return violations


def validate_ens_ascii(abs_path):
    """Check file for non-ASCII characters. Return (is_clean, error_text)."""
    try:
        vios = check_ascii_only(abs_path)
    except OSError as exc:
        return False, str(exc)
    if not vios:
        return True, ""
    lines = []
    lines.append(f"ASCII-ONLY VIOLATION in {abs_path}:")
    lines.append(f"  ENSDF files (.ens) MUST contain only standard ASCII characters.")
    lines.append(f"  {len(vios)} line(s) with non-ASCII characters found:")
    for lineno, text, chars in vios[:5]:
        unique = sorted(set(chars), key=ord)
        char_list = " ".join(f"U+{ord(c):04X} ({c!r})" for c in unique)
        snippet = text[:80]
        lines.append(f"    Line {lineno}: {char_list}")
        lines.append(f"      {snippet}")
    if len(vios) > 5:
        lines.append(f"    ... and {len(vios)-5} more line(s)")
    lines.append("")
    lines.append("  Fix: Replace non-ASCII characters with ASCII equivalents:")
    lines.append("    Unicode minus (U+2212) -> ASCII hyphen-minus (-)")
    lines.append("    Unicode asterisk (U+2217) -> ASCII asterisk (*)")
    lines.append("    Degree symbol (U+00B0) -> |' (ENSDF degree notation)")
    return False, "\n".join(lines)


def is_mutating_call(payload):
    """True only for calls that can rewrite .ens content.

    Read-only calls must never consume guard tokens: PreToolUse issues a
    token on each read and the immediately following edit depends on it.
    Popping tokens for read calls caused false
    "changed since your last read/edit (concurrent edit)" denials.
    """
    tool = payload.get("tool_name") or payload.get("toolName", "")
    if tool in EDIT_TOOLS or tool in PATCH_TOOLS:
        return True
    tool_input = payload.get("tool_input") or payload.get("toolArgs") or {}
    if not isinstance(tool_input, dict):
        return False
    command = tool_input.get("command")
    return isinstance(command, str) and "--dry-run" not in command and bool(MUTATING_RE.search(command))


def main():
    try:
        payload = load_input()
    except ValueError as exc:
        emit({"additionalContext": f"ENSDF post-tool hook could not parse event input: {exc}"})
        return
    tool = payload.get("tool_name") or payload.get("toolName", "")
    if not isinstance(tool, str) or not tool.strip():
        emit({"additionalContext": "ENSDF post-tool hook could not parse event input: no valid tool name."})
        return

    # Read-only calls: nothing to validate; the guard token must survive.
    if tool in ("read_file", "readFile", "read/readFile", "Read", "read", "view"):
        emit({})
        return

    # Collect all .ens files touched by this edit
    ens_paths = find_all_ens_paths(payload)
    if not ens_paths:
        emit({})
        return

    cwd = payload.get("cwd", "") or os.getcwd()
    is_failure = payload.get("hook_event_name") == "PostToolUseFailure" or "error" in payload
    if is_mutating_call(payload):
        mismatches, changed_or_untracked = pop_expected_hashes(ens_paths, cwd, is_failure)
    else:
        mismatches, changed_or_untracked = [], True
    if mismatches:
        files = "\n".join(f"  {path}" for path, _, _ in mismatches)
        if is_failure:
            context = (
                "The ENSDF tool action failed and changed the file from its pre-tool content "
                "to an unexpected or unverifiable result. It may have left partial changes; "
                "the action was not undone.\n"
            )
        else:
            context = (
                "ENSDF post-edit content differs from the PreToolUse prediction. "
                "The completed tool action was not undone. "
                "The edit may have collapsed, expanded, or otherwise rewritten an unintended block.\n"
            )
        emit({
            "additionalContext": (
                context +
                f"Affected file(s):\n{files}\n"
                "Re-read the affected block, inspect the diff, and rebuild a smaller exact edit."
            ),
        })
        return

    if is_failure and not changed_or_untracked:
        emit({})
        return

    # ===== PASS 1: ASCII-only validation (ALWAYS — data records AND comments) =====
    # Non-ASCII characters are forbidden in .ens files regardless of record type.
    ascii_errors = []
    for path in ens_paths:
        abs_path = resolve_path(path, cwd)
        if not os.path.isfile(abs_path):
            ascii_errors.append(f"ENSDF file is missing after the tool action: {abs_path}")
            continue
        clean, err = validate_ens_ascii(abs_path)
        if not clean:
            ascii_errors.append(err)

    if ascii_errors:
        error_text = "\n\n".join(ascii_errors)
        emit({
            "additionalContext": (
                "ENSDF ASCII validation failed after the tool action, which was not undone. "
                ".ens files must be readable and use standard ASCII.\n\n"
                f"{error_text}"
            ),
        })
        return

    # ===== PASS 2: 80-column ruler validation (DATA RECORDS ONLY) =====
    # Comments have no strict column requirements — skip for comment-only edits.
    if comment_only_edit(payload):
        emit({})
        return

    ruler_script = find_ruler_script(payload)

    all_errors = []
    for path in ens_paths:
        abs_path = resolve_path(path, cwd)
        if not os.path.isfile(abs_path):
            continue
        try:
            result = run_ruler(ruler_script, abs_path)
        except OSError as exc:
            all_errors.append(f"Could not run ENSDF ruler for {abs_path}: {exc}")
            continue
        if result.returncode != 0:
            output = (result.stdout + result.stderr).strip()
            all_errors.append(f"FILE: {abs_path}\n{output}")

    if not all_errors:
        emit({})
        return

    error_text = "\n\n".join(all_errors)
    emit({
        "additionalContext": (
            "ENSDF 80-column validation failed after the tool action, which was not undone. "
            "Fix the data-record edit before continuing.\n\n"
            "Sacred Workflow (ENSDF-Agent.agent.md — MANDATORY):\n"
            "  EDIT -> VALIDATE -> CONFIRM -> REPEAT\n\n"
            "Required steps:\n"
            "  1. Identify the misaligned field from the error output below.\n"
            "  2. Fix ONE field at a time using replace_string_in_file or editFiles.\n"
            '  3. Re-run: python .github/scripts/ensdf_1line_ruler.py --line "<fixed line>"\n'
            "  4. Confirm exit code 0 before proceeding to the next edit.\n\n"
            "Do NOT make multiple edits before validating each one.\n\n"
            f"Validation errors:\n{error_text}"
        ),
    })


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        emit({
            "additionalContext": (
                "ENSDF post-tool validation hook failed after the tool action; "
                f"the action was not undone: {exc}"
            ),
        })