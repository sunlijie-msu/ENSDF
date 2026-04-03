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

# --- Read stdin JSON ---
$stdin_content = $input | Out-String
if ([string]::IsNullOrWhiteSpace($stdin_content)) { exit 0 }

try {
    $hook_input = $stdin_content | ConvertFrom-Json -ErrorAction Stop
} catch {
    exit 0
}

# --- Only act on file creation tools ---
# VS Code uses "create_file" (snake_case) or "edit/createFile" (slash format)
$tool_name = $hook_input.tool_name
$is_create_tool = $tool_name -in @(
    "create_file",
    "edit/createFile"
)
if (-not $is_create_tool) { exit 0 }

# --- Extract file path and workspace root from hook input ---
$file_path       = $hook_input.tool_input.filePath
$workspace_root  = $hook_input.cwd

if ([string]::IsNullOrEmpty($file_path) -or [string]::IsNullOrEmpty($workspace_root)) { exit 0 }

# --- Resolve to absolute path if a relative path was supplied ---
if (-not [System.IO.Path]::IsPathRooted($file_path)) {
    $file_path = Join-Path $workspace_root $file_path
}

# --- Get the immediate parent directory of the target file ---
$parent_dir = [System.IO.Path]::GetDirectoryName($file_path)

# --- Normalize path separators and trailing separators for robust comparison ---
# GetDirectoryName() returns backslashes; cwd from hook input may use forward slashes.
# Unify both to backslashes before comparing.
$norm_parent = $parent_dir.Replace('/', '\').TrimEnd('\')
$norm_root   = $workspace_root.Replace('/', '\').TrimEnd('\')

# --- Check 1: workspace root ---
$is_root_violation = ($norm_parent -ieq $norm_root)

# --- Check 2: protected data trees ---
# A<N>/  — any mass-chain evaluation directory: A34, A35, A36, A60, A100, ...
#           Pattern: folder name = "A" followed by one or more digits.
# XUNDL/ — experimental unevaluated nuclear data list (Git submodule)
$is_data_violation = $false
$matched_dir = ''

# Extract the first path segment under the workspace root and test it.
if ($norm_parent.Length -gt $norm_root.Length) {
    $relative      = $norm_parent.Substring($norm_root.Length).TrimStart('\')
    $first_segment = $relative.Split('\')[0]

    if ($first_segment -match '^A\d+$' -or $first_segment -ieq 'XUNDL') {
        $is_data_violation = $true
        $matched_dir = $first_segment
    }
}

if (-not ($is_root_violation -or $is_data_violation)) { exit 0 }

# --- Build denial response ---
$file_name = [System.IO.Path]::GetFileName($file_path)

if ($is_root_violation) {
    $violation_detail = @(
        "Reason: Creating files directly in the workspace root is not allowed.",
        "Target: $file_name",
        "Root:   $norm_root"
    ) -join "`n"
} else {
    $violation_detail = @(
        "Reason: Creating files inside the protected $matched_dir/ tree is not allowed.",
        "Target: $norm_parent\$file_name",
        "Policy: $matched_dir/ contains evaluated nuclear data files (new/, old/, raw/, pdf/).",
        "        These files must be managed through the ENSDF evaluation workflow,",
        "        not created directly by AI tooling."
    ) -join "`n"
}

$reason = @(
    "BLOCKED by workspace security hook (block-root-file-creation).",
    "",
    $violation_detail,
    "",
    "Allowed location for AI-generated files:",
    "  .github/temp/   — temporary scripts and analysis files only"
) -join "`n"

$output = [ordered]@{
    hookSpecificOutput = [ordered]@{
        hookEventName            = "PreToolUse"
        permissionDecision       = "deny"
        permissionDecisionReason = $reason
    }
} | ConvertTo-Json -Depth 3

Write-Output $output
exit 0
