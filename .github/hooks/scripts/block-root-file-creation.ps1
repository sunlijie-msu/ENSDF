# ENSDF Workspace Hook: Block file creation in protected directories
# -----------------------------------------------------------------------
# Prevents any AI action from creating new files in protected directories.
#
# Hook event : PreToolUse
# Blocks     : create_file / edit/createFile when filePath resolves to:
#              (1) The workspace root directory
#              (2) Any path under A<N>/ (A34, A35, A100, ... any mass number)
#              (3) Any path under XUNDL/
# Allows     : File creation under .github/ (e.g. .github/temp/)
#              and any other non-protected subdirectory
#
# Output     : JSON with permissionDecision "deny" — blocks the single tool
#              call without stopping the agent session.
# -----------------------------------------------------------------------

param()

# Keep one implementation for all platforms. The Python hook fails closed and
# handles all supported tool-input shapes.
$python_script = Join-Path $PSScriptRoot 'block-root-file-creation.py'
$stdin_content = [Console]::In.ReadToEnd()
if ([string]::IsNullOrWhiteSpace($stdin_content)) { exit 0 }

$stdin_content | & python $python_script
exit $LASTEXITCODE
