# ENSDF-Agent Hook: Block git restore/checkout for error recovery
# -----------------------------------------------------------------------
# Enforces the Error Recovery Protocol in ENSDF-Agent.agent.md:
#   "Do NOT use 'git restore' or 'git checkout' to fix mistakes."
#
# Hook event : PreToolUse
# Blocks     : git restore (any form)
#            : git checkout -- <path>   (explicit file-restoration form)
#            : git checkout .           (restore entire working tree)
# Allows     : git checkout <branch>   (legitimate branch switching)
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

# --- Only act on terminal execution tools ---
$tool_name = $hook_input.tool_name
$is_terminal_tool = $tool_name -in @(
    "execute/runInTerminal",
    "runInTerminal",
    "run_in_terminal"
)
if (-not $is_terminal_tool) { exit 0 }

# --- Extract the command string ---
$command = $hook_input.tool_input.command
if ([string]::IsNullOrEmpty($command)) { exit 0 }

# Normalize: collapse internal whitespace so multi-space won't evade patterns
$cmd = ($command.Trim() -replace '\s+', ' ')

# --- Pattern matching ---
# Pattern 1: git restore — exclusively a file-restoration command
$block_restore       = $cmd -match '(?i)\bgit\s+restore\b'

# Pattern 2: git checkout -- <path> — explicit restoration form (note the --)
$block_checkout_file = $cmd -match '(?i)\bgit\s+checkout\s+--\s'

# Pattern 3: git checkout . — restore all tracked files in the working tree
$block_checkout_dot  = $cmd -match '(?i)\bgit\s+checkout\s+\.'

$is_blocked = $block_restore -or $block_checkout_file -or $block_checkout_dot

if (-not $is_blocked) { exit 0 }

# --- Build denial response ---
$reason = @(
    'BLOCKED by ENSDF-Agent security hook.',
    '',
    'From ENSDF-Agent.agent.md (Error Recovery Protocol — Mandatory):',
    '  "Nuclear data tasks require high-precision work, not typical',
    '  software development tasks. Do NOT use `git restore` or',
    '  `git checkout` to fix mistakes. You must identify and fix errors',
    '  carefully to maintain absolute rigor."',
    '',
    'Mandatory steps:',
    '  1. Identify the root cause through analysis, not reversion.',
    '  2. Fix errors using replace_string_in_file or multi_replace_string_in_file.',
    '  3. Validate with column_calibrate.py and ensdf_1line_ruler.py.',
    '  4. Let user review diffs in VS Code diff viewer before accepting changes.',
    '',
    'Rationale: Reversion bypasses the VS Code diff viewer, eliminating',
    'the mandatory human review layer that catches LLM formatting mistakes',
    'in nuclear data files.'
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
