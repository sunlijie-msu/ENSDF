#!/usr/bin/env python3
"""
ENSDF Workspace Hook: Block file creation in protected directories (cross-platform)
-----------------------------------------------------------------------
Python port of block-root-file-creation.ps1 for Linux/macOS compatibility.

Hook event : PreToolUse
Blocks     : create_file / edit/createFile when filePath resolves to:
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


def load_input():
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def main():
    hook_input = load_input()
    if not hook_input:
        sys.exit(0)

    # --- Only act on file creation tools ---
    tool_name = hook_input.get("tool_name", "")
    if tool_name not in ("create_file", "edit/createFile"):
        sys.exit(0)

    # --- Extract file path and workspace root ---
    tool_input = hook_input.get("tool_input", {})
    file_path = tool_input.get("filePath", "")
    workspace_root = hook_input.get("cwd", "")

    if not file_path or not workspace_root:
        sys.exit(0)

    # --- Resolve to absolute path if relative ---
    if not os.path.isabs(file_path):
        file_path = os.path.join(workspace_root, file_path)

    # --- Normalize separators and get parent directory ---
    file_path = os.path.normpath(file_path)
    workspace_root = os.path.normpath(workspace_root)
    parent_dir = os.path.dirname(file_path)

    # --- Check 1: workspace root ---
    is_root_violation = (parent_dir.lower() == workspace_root.lower())

    # --- Check 2: protected data trees ---
    is_data_violation = False
    matched_dir = ""

    if len(parent_dir) > len(workspace_root):
        relative = parent_dir[len(workspace_root):].lstrip(os.sep).lstrip("/")
        first_segment = relative.replace("\\", "/").split("/")[0]
        if re.match(r"^A\d+$", first_segment):
            is_data_violation = True
            matched_dir = first_segment
        elif first_segment.upper() == "XUNDL":
            is_data_violation = True
            matched_dir = first_segment

    if not (is_root_violation or is_data_violation):
        sys.exit(0)

    # --- Build denial response ---
    file_name = os.path.basename(file_path)

    if is_root_violation:
        violation_detail = (
            f"Reason: Creating files directly in the workspace root is not allowed.\n"
            f"Target: {file_name}\n"
            f"Root:   {workspace_root}"
        )
    else:
        violation_detail = (
            f"Reason: Creating files inside the protected {matched_dir}/ tree is not allowed.\n"
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

    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }
    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
