#!/usr/bin/env python3
"""
ENSDF Workspace Hook: Block file creation in protected directories (cross-platform)
-----------------------------------------------------------------------
Python port of block-root-file-creation.ps1 for Linux/macOS compatibility.

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


CREATE_TOOL_NAMES = {
    "create_file",
    "createFile",
    "edit/createFile",
    "functions.create_file",
    "vscode.createFile",
}
PATCH_TOOL_NAMES = {"apply_patch", "edit/applyPatch", "functions.apply_patch"}


def load_input():
    raw = sys.stdin.read().strip()
    if not raw:
        return {}, ""
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return {}, "Hook input was not valid JSON; file creation was blocked."
    if not isinstance(payload, dict):
        return {}, "Hook input was not a JSON object; file creation was blocked."
    return payload, ""


def emit_denial(reason):
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }
    print(json.dumps(output))


def default_workspace_root():
    # This file lives at <workspace>/.github/hooks/scripts/.
    return os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )


def resolve_path(file_path, workspace_root):
    if not os.path.isabs(file_path):
        file_path = os.path.join(workspace_root, file_path)
    return os.path.realpath(os.path.normpath(file_path))


def classify_path(file_path, workspace_root):
    """Return (violation_kind, matched_directory, absolute_path)."""
    absolute_path = resolve_path(file_path, workspace_root)
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
    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return []

    if tool_name in CREATE_TOOL_NAMES:
        for key in ("filePath", "file_path", "path"):
            value = tool_input.get(key)
            if isinstance(value, str) and value.strip():
                return [(value, "create_file")]
        return []

    if tool_name in PATCH_TOOL_NAMES:
        patch_text = tool_input.get("input", "")
        if not isinstance(patch_text, str):
            return []
        paths = []
        for match in re.finditer(r"^\*\*\* Add File:\s*(.+?)\s*$", patch_text, re.MULTILINE):
            paths.append((match.group(1), "apply_patch add-file"))
        return paths

    return []


def main():
    hook_input, parse_error = load_input()
    if parse_error:
        emit_denial(
            "BLOCKED by workspace security hook (block-root-file-creation).\n\n"
            + parse_error
        )
        sys.exit(0)
    if not hook_input:
        sys.exit(0)

    target_paths = extract_target_paths(hook_input)
    if not target_paths:
        sys.exit(0)

    workspace_root = hook_input.get("cwd") or default_workspace_root()
    workspace_root = os.path.realpath(os.path.normpath(workspace_root))

    for file_path, operation in target_paths:
        violation, matched_dir, absolute_path = classify_path(file_path, workspace_root)
        if not violation:
            continue

        parent_dir = os.path.dirname(absolute_path)
        file_name = os.path.basename(absolute_path)
        if violation == "root":
            violation_detail = (
                f"Reason: Creating files directly in the workspace root is not allowed.\n"
                f"Operation: {operation}\n"
                f"Target: {file_name}\n"
                f"Root:   {workspace_root}"
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
    main()
