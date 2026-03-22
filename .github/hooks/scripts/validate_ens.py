import json
import os
import re
import subprocess
import sys
import difflib

# ENSDF FRIBND Agent Hook: Validate .ens files after edits
# --------------------------------------------------------
# PostToolUse event — runs ensdf_1line_ruler.py on any .ens file that was
# just created or edited by the FRIBND agent.
#
# Key features:
#   - Handles all VS Code file-editing tool input shapes
#     (replace_string_in_file, multi_replace_string_in_file, create_file,
#      apply_patch, edit/editFiles)
#   - Validates ALL .ens files touched by a single tool call (multi-file)
#   - Uses hook-provided cwd for robust script path resolution
#   - Skips validation for comment-only edits (per FRIBND.agent.md)
#   - Returns Sacred Workflow guidance on failure
#
# Hook event : PostToolUse
# On failure : decision "block" + Sacred Workflow steps in reason
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
    sys.stdout.write(json.dumps(payload))


def load_input():
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def find_all_ens_paths(payload):
    """Collect all unique .ens file paths touched by this tool call.

    Handles four input shapes:
      - replace_string_in_file / create_file  → tool_input.filePath
      - multi_replace_string_in_file          → tool_input.replacements[*].filePath
      - apply_patch                           → *** Update/Add File: <path> headers
      - TOOL_INPUT_FILE_PATH env var          → set by some integrations
    """
    paths = set()
    tool_input = payload.get("tool_input") or {}

    # Environment variable override (used by some Claude Code integrations)
    env_path = os.environ.get("TOOL_INPUT_FILE_PATH", "")
    if env_path and env_path.lower().endswith(".ens"):
        paths.add(env_path)

    # replace_string_in_file / create_file → tool_input.filePath
    for key in ("filePath", "file_path"):
        value = tool_input.get(key)
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
    patch_text = tool_input.get("input")
    if isinstance(patch_text, str):
        for match in re.finditer(r"\*\*\* (?:Update|Add) File: (.+)", patch_text):
            path = match.group(1).strip()
            if path.lower().endswith(".ens"):
                paths.add(path)

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
    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input") or {}

    if tool_name == "apply_patch":
        patch_text = tool_input.get("input", "")
        if isinstance(patch_text, str):
            return extract_changed_lines_from_patch(patch_text)

    changed = []

    old_string = tool_input.get("oldString")
    new_string = tool_input.get("newString")
    if isinstance(old_string, str) and isinstance(new_string, str):
        changed.extend(extract_changed_lines_from_pair(old_string, new_string))

    content = tool_input.get("content")
    if isinstance(content, str):
        changed.extend(content.splitlines())

    replacements = tool_input.get("replacements")
    if isinstance(replacements, list):
        for item in replacements:
            if not isinstance(item, dict):
                continue
            old_string = item.get("oldString")
            new_string = item.get("newString")
            if isinstance(old_string, str) and isinstance(new_string, str):
                changed.extend(extract_changed_lines_from_pair(old_string, new_string))

    return changed


def is_comment_record(line):
    return len(line) >= 8 and line[7] == "c"


def is_noncomment_record(line):
    return len(line) >= 8 and line[7] != "c" and not line.isspace()


def comment_only_edit(payload):
    """Return True if ALL changed non-blank ENSDF records are comment (cL/cG) lines.

    Per FRIBND.agent.md: 'Skip ruler, column validation, and gamma ordering
    checks only if task is purely editing comments.'
    """
    changed_lines = extract_all_changed_lines(payload)
    record_lines = [line for line in changed_lines if len(line) >= 8]
    if not record_lines:
        return False
    return all(is_comment_record(line) for line in record_lines)


def find_ruler_script(payload):
    """Locate ensdf_1line_ruler.py, preferring the cwd provided by VS Code."""
    cwd = payload.get("cwd", "") or os.getcwd()
    candidate = os.path.join(cwd, ".github", "scripts", "ensdf_1line_ruler.py")
    if os.path.isfile(candidate):
        return candidate
    # Fallback to relative path (works when subprocess cwd is workspace root)
    return os.path.join(".github", "scripts", "ensdf_1line_ruler.py")


def run_ruler(ruler_script, file_path):
    return subprocess.run(
        [sys.executable, ruler_script, "--file", file_path, "--show-only-wrong"],
        capture_output=True,
        text=True,
        check=False,
    )


def resolve_path(path, cwd):
    """Resolve a potentially relative path against a base directory."""
    if os.path.isabs(path):
        return path
    return os.path.normpath(os.path.join(cwd, path))


def main():
    payload = load_input()

    # Collect all .ens files touched by this edit
    ens_paths = find_all_ens_paths(payload)
    if not ens_paths:
        emit({})
        return

    # Per FRIBND.agent.md: skip validation for comment-only edits
    if comment_only_edit(payload):
        emit({})
        return

    ruler_script = find_ruler_script(payload)
    cwd = payload.get("cwd", "") or os.getcwd()

    all_errors = []
    for path in ens_paths:
        abs_path = resolve_path(path, cwd)
        if not os.path.isfile(abs_path):
            continue
        result = run_ruler(ruler_script, abs_path)
        if result.returncode != 0:
            output = (result.stdout + result.stderr).strip()
            all_errors.append(f"FILE: {abs_path}\n{output}")

    if not all_errors:
        emit({})
        return

    error_text = "\n\n".join(all_errors)
    emit({
        "decision": "block",
        "reason": (
            "ENSDF 80-column validation failed. Fix the data-record edit before continuing.\n\n"
            "Sacred Workflow (FRIBND.agent.md — MANDATORY):\n"
            "  EDIT -> VALIDATE -> CONFIRM -> REPEAT\n\n"
            "Required steps:\n"
            "  1. Identify the misaligned field from the error output below.\n"
            "  2. Fix ONE field at a time using replace_string_in_file.\n"
            '  3. Re-run: python .github/scripts/ensdf_1line_ruler.py --line "<fixed line>"\n'
            "  4. Confirm exit code 0 before proceeding to the next edit.\n\n"
            "Do NOT make multiple edits before validating each one.\n\n"
            f"Validation errors:\n{error_text}"
        ),
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": f"ensdf_1line_ruler.py FAILED:\n{error_text}",
        },
    })


if __name__ == "__main__":
    main()