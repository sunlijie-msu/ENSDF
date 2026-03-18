import json
import os
import re
import subprocess
import sys
import difflib


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


def find_file_path(payload):
    env_path = os.environ.get("TOOL_INPUT_FILE_PATH", "")
    if env_path:
        return env_path

    tool_input = payload.get("tool_input") or {}
    for key in ("filePath", "file_path"):
        value = tool_input.get(key)
        if isinstance(value, str) and value:
            return value

    patch_text = tool_input.get("input")
    if isinstance(patch_text, str):
        match = re.search(r"\*\*\* (?:Update|Add) File: (.+)", patch_text)
        if match:
            return match.group(1).strip()

    return ""


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


def extract_changed_lines(payload):
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
    changed_lines = extract_changed_lines(payload)
    record_lines = [line for line in changed_lines if len(line) >= 8]
    if not record_lines:
        return False
    return all(is_comment_record(line) for line in record_lines)


def run_ruler(file_path):
    return subprocess.run(
        [
            sys.executable,
            ".github/scripts/ensdf_1line_ruler.py",
            "--file",
            file_path,
            "--show-only-wrong",
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def main():
    payload = load_input()
    file_path = find_file_path(payload)

    if not file_path or not file_path.lower().endswith(".ens"):
        emit({})
        return

    if comment_only_edit(payload):
        emit({})
        return

    result = run_ruler(file_path)
    if result.returncode == 0:
        emit({})
        return

    output = (result.stdout + result.stderr).strip()
    emit(
        {
            "decision": "block",
            "reason": "ENSDF 80-column validation failed. Fix the data-record edit before continuing.",
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": f"ensdf_1line_ruler.py FAILED on {file_path}:\n{output}",
            },
        }
    )


if __name__ == "__main__":
    main()