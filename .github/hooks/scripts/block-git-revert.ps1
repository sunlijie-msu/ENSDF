# ENSDF-Agent Hook: Block git restore/checkout for error recovery
# -----------------------------------------------------------------------
# Enforces the Error Recovery Protocol in ENSDF-Agent.agent.md:
#   "Do NOT use 'git restore' or 'git checkout' on critical .ens files."
#
# Hook event : PreToolUse
# Blocks     : git restore/checkout that can affect .ens files
#            : git restore/checkout that target non-temp paths
#            : broad or ambiguous git restore/checkout forms
#            : git -C <path> restore/checkout and similar option-prefixed forms
#            : common wrapped shell forms such as cmd /c, powershell -Command,
#              bash -c, and pwsh -Command when they invoke git restore/checkout
# Allows     : explicit temp script/code paths that do not touch .ens files
#            : unrelated terminal commands that merely mention those words as text
#
# Output     : JSON with permissionDecision "deny" - blocks the single tool
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

# Normalize: collapse whitespace but preserve separators so chained commands can
# still be analyzed segment-by-segment.
$cmd = (($command -replace "[`r`n]+", ' ') -replace '\s+', ' ').Trim()

function Unquote-Token {
    param([string]$Token)

    if ([string]::IsNullOrEmpty($Token)) { return $Token }
    if ($Token.Length -ge 2) {
        if (($Token.StartsWith('"') -and $Token.EndsWith('"')) -or
            ($Token.StartsWith("'") -and $Token.EndsWith("'"))) {
            return $Token.Substring(1, $Token.Length - 2)
        }
    }

    return $Token
}

function Get-CommandTokens {
    param([string]$Text)

    $matches = [regex]::Matches($Text, '"[^"]*"|''[^'']*''|&&|\|\||[;|&]|[^\s;|&]+')
    return $matches | ForEach-Object { $_.Value }
}

function Normalize-PathToken {
    param([string]$Token)

    $normalized = Unquote-Token $Token
    if ([string]::IsNullOrWhiteSpace($normalized)) { return '' }

    $normalized = $normalized.Trim()
    if ($normalized.StartsWith('./')) {
        $normalized = $normalized.Substring(2)
    }

    return ($normalized -replace '\\', '/').Trim()
}

function Is-EnsPathSpec {
    param([string]$Token)

    $normalized = Normalize-PathToken $Token
    if ([string]::IsNullOrWhiteSpace($normalized)) { return $false }

    return $normalized -match '(?i)(^|/)[^/]*\.ens$'
}

function Is-TempPathSpec {
    param([string]$Token)

    $normalized = Normalize-PathToken $Token
    if ([string]::IsNullOrWhiteSpace($normalized)) { return $false }
    if ($normalized -in @('.', '*')) { return $false }

    return $normalized -match '(?i)(^|/)(temp|tmp)(/|$)'
}

function Is-StrongTempFilePath {
    param([string]$Token)

    $normalized = Normalize-PathToken $Token
    if (-not (Is-TempPathSpec $normalized)) { return $false }

    return $normalized -match '(?i)(^|/)[^/]+\.[A-Za-z0-9_*?-]+$'
}

function Get-SubcommandOptionValueCount {
    param(
        [string]$Subcommand,
        [string]$OptionToken
    )

    $option = $OptionToken.ToLowerInvariant()

    switch ($Subcommand) {
        'restore' {
            if ($option -in @('-s', '--source', '-u', '--unified', '--inter-hunk-context', '--pathspec-from-file')) {
                return 1
            }
        }
        'checkout' {
            if ($option -in @('-b', '-B', '--orphan', '--conflict', '--pathspec-from-file')) {
                return 1
            }
        }
    }

    return 0
}

function Get-GitPathSpecs {
    param(
        [string[]]$Segment,
        [int]$SubcommandIndex,
        [string]$Subcommand
    )

    $pathSpecs = New-Object System.Collections.Generic.List[string]
    $sawDoubleDash = $false

    for ($i = $SubcommandIndex + 1; $i -lt $Segment.Count; $i++) {
        $token = Unquote-Token $Segment[$i]
        if ([string]::IsNullOrWhiteSpace($token)) { continue }

        if ($token -eq '--') {
            $sawDoubleDash = $true
            continue
        }

        if (-not $sawDoubleDash) {
            if ($token.StartsWith('-')) {
                $skipCount = Get-SubcommandOptionValueCount -Subcommand $Subcommand -OptionToken $token
                $i += $skipCount
                continue
            }

            if ($Subcommand -eq 'checkout' -and -not (Is-StrongTempFilePath $token)) {
                return [pscustomobject]@{
                    PathSpecs   = @()
                    IsAmbiguous = $true
                }
            }
        }

        $pathSpecs.Add($token)
    }

    return [pscustomobject]@{
        PathSpecs   = @($pathSpecs)
        IsAmbiguous = $false
    }
}

function Get-BlockedGitCommand {
    param(
        [string]$Text,
        [int]$Depth = 0
    )

    if ([string]::IsNullOrWhiteSpace($Text) -or $Depth -gt 2) { return $null }

    $tokens = @(Get-CommandTokens -Text $Text)
    if ($tokens.Count -eq 0) { return $null }

    $segments = @()
    $currentSegment = @()

    foreach ($token in $tokens) {
        if ($token -in @(';', '|', '&', '&&', '||')) {
            if ($currentSegment.Count -gt 0) {
                $segments += ,@($currentSegment)
                $currentSegment = @()
            }
            continue
        }

        $currentSegment += $token
    }

    if ($currentSegment.Count -gt 0) {
        $segments += ,@($currentSegment)
    }

    foreach ($segment in $segments) {
        for ($i = 0; $i -lt $segment.Count; $i++) {
            $token = Unquote-Token $segment[$i]

            if ($token -match '^(?i)(powershell|pwsh|cmd|bash|sh|zsh)$') {
                for ($j = $i + 1; $j -lt $segment.Count - 1; $j++) {
                    $wrapperArg = Unquote-Token $segment[$j]
                    if ($wrapperArg -match '^(?i)(-command|-c|/c)$') {
                        $nestedText = Unquote-Token $segment[$j + 1]
                        $nestedMatch = Get-BlockedGitCommand -Text $nestedText -Depth ($Depth + 1)
                        if ($nestedMatch) { return $nestedMatch }
                        break
                    }
                }
            }
        }

        for ($i = 0; $i -lt $segment.Count; $i++) {
            $token = Unquote-Token $segment[$i]

            if ($token -notmatch '(?i)(^|[\\/])git(?:\.exe)?$') { continue }

            for ($j = $i + 1; $j -lt $segment.Count; $j++) {
                $nextToken = Unquote-Token $segment[$j]
                if ([string]::IsNullOrWhiteSpace($nextToken)) { continue }

                if ($nextToken -match '^(?i)(-c|-C|--config-env)$') {
                    $j++
                    continue
                }

                if ($nextToken -match '^(?i)(--git-dir|--work-tree|--namespace|--super-prefix)$') {
                    $j++
                    continue
                }

                if ($nextToken.StartsWith('-')) { continue }

                if ($nextToken -match '^(?i)(checkout|restore)$') {
                    $subcommand = $nextToken.ToLowerInvariant()
                    $pathInfo = Get-GitPathSpecs -Segment $segment -SubcommandIndex $j -Subcommand $subcommand
                    $pathSpecs = @($pathInfo.PathSpecs)

                    if ($pathInfo.IsAmbiguous) {
                        return [pscustomobject]@{
                            Subcommand = $subcommand
                            PathSpecs  = @()
                            ReasonCode = 'ambiguous'
                        }
                    }

                    if ($pathSpecs.Count -eq 0) {
                        return [pscustomobject]@{
                            Subcommand = $subcommand
                            PathSpecs  = @()
                            ReasonCode = 'broad'
                        }
                    }

                    if ($pathSpecs | Where-Object { Is-EnsPathSpec $_ }) {
                        return [pscustomobject]@{
                            Subcommand = $subcommand
                            PathSpecs  = $pathSpecs
                            ReasonCode = 'ens'
                        }
                    }

                    if ($pathSpecs | Where-Object { -not (Is-TempPathSpec $_) }) {
                        return [pscustomobject]@{
                            Subcommand = $subcommand
                            PathSpecs  = $pathSpecs
                            ReasonCode = 'non-temp'
                        }
                    }

                    break
                }

                break
            }
        }
    }

    return $null
}

$blockedCommandInfo = Get-BlockedGitCommand -Text $cmd
if (-not $blockedCommandInfo) { exit 0 }

$blockedCommand = "git $($blockedCommandInfo.Subcommand)"
$commandExcerpt = if ($cmd.Length -gt 220) {
    $cmd.Substring(0, 220) + '...'
} else {
    $cmd
}

$targetSummary = if ($blockedCommandInfo.PathSpecs.Count -gt 0) {
    'Target paths:' + "`n" + (($blockedCommandInfo.PathSpecs | ForEach-Object { '  ' + (Normalize-PathToken $_) }) -join "`n")
} else {
    'Target paths: none explicitly identified.'
}

$whyBlocked = switch ($blockedCommandInfo.ReasonCode) {
    'ens' {
        'This command is blocked because it targets one or more .ens nuclear dataset files.'
    }
    'non-temp' {
        'This command is blocked because at least one target path is outside a temp folder.'
    }
    'ambiguous' {
        'This command is blocked because `git checkout` without an explicit temp file path is ambiguous and could switch branches or affect critical files.'
    }
    default {
        'This command is blocked because it does not explicitly limit itself to temp script/code paths.'
    }
}

# --- Build denial response ---
$reason = @(
    'BLOCKED by ENSDF-Agent security hook.',
    '',
    "Blocked command: $blockedCommand",
    'Command excerpt:',
    "  $commandExcerpt",
    '',
    $targetSummary,
    '',
    $whyBlocked,
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
    '  2. If the target is an .ens or other working file, identify the root cause through analysis, not reversion.',
    '  3. Fix errors using replace_string_in_file or multi_replace_string_in_file.',
    '  4. Validate .ens fixes with column_calibrate.py and ensdf_1line_ruler.py.',
    '  5. Use diff-aware edits so that users can review diffs in VS Code diff viewer before accepting changes.',
    '',
    'If branch switching is explicitly requested by the user, use `git switch`,',
    'not `git checkout`.',
    '',
    'Rationale: Reversion bypasses the VS Code diff viewer, eliminating',
    'the mandatory human review layer that catches LLM formatting mistakes',
    'in nuclear data files.'
) -join "`n"

$shortReason = 'Git restore/checkout is forbidden in .ens file editing tasks. Read the denial message and repair the file in place.'

$output = [ordered]@{
    continue = $false
    stopReason = $reason
    systemMessage = $reason
    hookSpecificOutput = [ordered]@{
        hookEventName            = "PreToolUse"
        permissionDecision       = "deny"
        permissionDecisionReason = $reason
    }
} | ConvertTo-Json -Depth 3

Write-Output $output
exit 0
