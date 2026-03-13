# =============================================================================
# Validate Output - AI Project Rules Generator
# =============================================================================
# Validates generated .cursorrules and AGENTS.md files with heuristic scoring.
# Usage: .\scripts\validate-output.ps1 [-Path <project-root>] [-Strict] [-Threshold <n>]
# =============================================================================

param(
    [string]$Path = ".",
    [switch]$Strict,
    [int]$Threshold = -1
)

$ErrorActionPreference = "Stop"

$script:TotalChecks = 0
$script:PassedChecks = 0
$script:Warnings = @()
$script:Errors = @()

$PlaceholderPatterns = @(
    '\{[A-Z0-9_ -]+\}',
    '\{project',
    '___',
    '\bTBD\b',
    '\bTODO\b'
)

$VaguePatterns = @(
    'write good code',
    'write clean code',
    'follow best practices',
    'be professional',
    '\betc\.\b'
)

$HardcodedSkillPattern = '@[a-z0-9][a-z0-9-]*'
$HardcodedSkillIgnoreMarkers = @('Hardcoding', 'BAD', 'Anti-Pattern', 'Instead Do')
$RepoLocalPrefixes = @(
    'README.md',
    'AGENTS.md',
    '.cursorrules',
    'CHANGELOG.md',
    'setup.ps1',
    'setup.sh',
    'workflows/',
    'templates/',
    'scripts/',
    'i18n/',
    'images/',
    'log/'
)

$RequiredHeadings = @{
    ".cursorrules" = @("Project Identity", "Project Structure", "Coding Standards", "Critical Rules", "Code Smells")
    "AGENTS.md"    = @("Quick Context", "Skills", "Output", "Patterns", "Constraints")
}

function Pass([string]$Message) {
    $script:PassedChecks++
    $script:TotalChecks++
    Write-Host "  [PASS] $Message" -ForegroundColor Green
}

function Fail([string]$Message) {
    $script:TotalChecks++
    $script:Errors += $Message
    Write-Host "  [FAIL] $Message" -ForegroundColor Red
}

function Warn([string]$Message) {
    $script:Warnings += $Message
    Write-Host "  [WARN] $Message" -ForegroundColor Yellow
}

function Get-ConfigThreshold([string]$RootPath) {
    $configPath = Join-Path $RootPath ".rulesrc.yaml"
    if (-not (Test-Path $configPath)) {
        return $null
    }

    $content = Get-Content $configPath -Raw
    $match = [regex]::Match($content, '(?m)^\s*quality_threshold\s*:\s*(\d+)\s*$')
    if ($match.Success) {
        return [int]$match.Groups[1].Value
    }

    return $null
}

function Get-EffectiveThreshold([string]$RootPath, [int]$CliThreshold, [switch]$StrictMode) {
    if ($CliThreshold -ge 0) {
        $effective = $CliThreshold
    }
    else {
        $configured = Get-ConfigThreshold -RootPath $RootPath
        if ($null -ne $configured) {
            $effective = $configured
        }
        else {
            $effective = 38
        }
    }

    if ($StrictMode -and $effective -lt 42) {
        return 42
    }

    return $effective
}

function Strip-FencedCodeBlocks([string]$Content) {
    return [regex]::Replace($Content, '(?s)```.*?```', '')
}

function Get-PatternMatches([string]$Content, [string[]]$Patterns) {
    $results = New-Object System.Collections.Generic.List[string]
    foreach ($pattern in $Patterns) {
        foreach ($match in [regex]::Matches($Content, $pattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)) {
            $results.Add($match.Value)
        }
    }
    return @($results)
}

function Get-RepoLocalPathErrors([string]$Content, [string]$RootPath) {
    $candidates = New-Object System.Collections.Generic.HashSet[string]
    $errors = New-Object System.Collections.Generic.List[string]

    foreach ($match in [regex]::Matches($Content, '\[[^\]]+\]\(([^)]+)\)')) {
        $candidates.Add($match.Groups[1].Value) | Out-Null
    }

    foreach ($match in [regex]::Matches($Content, '`([^`\r\n]+)`')) {
        $candidates.Add($match.Groups[1].Value) | Out-Null
    }

    foreach ($candidate in $candidates) {
        $pathCandidate = $candidate.Trim()
        if ([string]::IsNullOrWhiteSpace($pathCandidate)) {
            continue
        }

        if ($pathCandidate -match '^(https?:|mailto:|#)') {
            continue
        }

        $normalized = $pathCandidate -replace '\\', '/'
        $normalized = $normalized.Split('#')[0]
        if ([string]::IsNullOrWhiteSpace($normalized)) {
            continue
        }

        if ($normalized.Contains('*') -or $normalized.Contains('{') -or $normalized.Contains('}')) {
            continue
        }

        $isRepoLocal = $false
        foreach ($prefix in $RepoLocalPrefixes) {
            if ($normalized -eq $prefix -or $normalized.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
                $isRepoLocal = $true
                break
            }
        }

        if (-not $isRepoLocal) {
            continue
        }

        $targetPath = Join-Path $RootPath ($normalized -replace '/', [IO.Path]::DirectorySeparatorChar)
        if (-not (Test-Path $targetPath)) {
            $errors.Add($normalized)
        }
    }

    return @($errors | Sort-Object -Unique)
}

function Get-HeadingCount([string]$Content) {
    return ([regex]::Matches($Content, '(?m)^#{1,6}\s+')).Count
}

function Get-TableCount([string]$Content) {
    return ([regex]::Matches($Content, '(?m)^\|.+\|\s*$')).Count
}

function Get-CodeBlockCount([string]$Content) {
    return ([regex]::Matches($Content, '(?m)^```')).Count / 2
}

function Get-BulletLineCount([string]$Content) {
    return ([regex]::Matches($Content, '(?m)^\s*([-*]|\d+\.)\s+')).Count
}

function Get-LongParagraphBlockCount([string]$Content) {
    $blocks = [regex]::Split($Content, "(\r?\n){2,}")
    $count = 0

    foreach ($block in $blocks) {
        $lines = @(
            $block -split "\r?\n" |
            Where-Object { $_.Trim() -ne "" }
        )

        if ($lines.Count -lt 10) {
            continue
        }

        $paragraphLines = @(
            $lines | Where-Object {
                $_ -notmatch '^\s*(#|>|[-*]|\d+\.|\|)'
            }
        )

        if ($paragraphLines.Count -ge 10) {
            $count++
        }
    }

    return $count
}

function Get-MeaningfulLines([string]$Content) {
    $lines = New-Object System.Collections.Generic.List[string]
    foreach ($line in ($Content -split "\r?\n")) {
        $trimmed = $line.Trim()
        if ($trimmed.Length -lt 30) {
            continue
        }
        if ($trimmed -match '^\|[- :]+\|?$') {
            continue
        }
        if ($trimmed -match '^(```|#|>|[-*]|\d+\.)') {
            continue
        }
        $lines.Add($trimmed)
    }
    return @($lines | Sort-Object -Unique)
}

function Get-HardcodedSkillHits([string]$Content) {
    $sanitized = Strip-FencedCodeBlocks $Content
    $hits = New-Object System.Collections.Generic.List[string]

    foreach ($line in ($sanitized -split "\r?\n")) {
        $skip = $false
        foreach ($marker in $HardcodedSkillIgnoreMarkers) {
            if ($line -match [regex]::Escape($marker)) {
                $skip = $true
                break
            }
        }
        if ($skip) {
            continue
        }

        foreach ($match in [regex]::Matches($line, $HardcodedSkillPattern)) {
            $hits.Add($match.Value)
        }
    }

    return @($hits | Sort-Object -Unique)
}

function Test-RequiredHeading([string]$Content, [string]$Heading) {
    return $Content -match [regex]::Escape($Heading)
}

function New-FileEvaluation([string]$FileName, [string]$RootPath) {
    $fullPath = Join-Path $RootPath $FileName
    $evaluation = [ordered]@{
        FileName          = $FileName
        Exists            = $false
        Content           = ""
        SanitizedContent  = ""
        LineCount         = 0
        HeadingCount      = 0
        TableCount        = 0
        CodeBlockCount    = 0
        BulletCount       = 0
        LongParagraphs    = 0
        RequiredFound     = @()
        MissingHeadings   = @()
        PlaceholderHits   = @()
        VagueHits         = @()
        HardcodedHits     = @()
        RepoPathErrors    = @()
        Scores            = [ordered]@{
            Completeness = 0
            Accuracy     = 0
            Specificity  = 0
            Scannability = 0
            Consistency  = 0
            Total        = 0
        }
        DuplicationCount  = 0
    }

    if (-not (Test-Path $fullPath)) {
        $msg = "Missing $FileName"
        Fail $msg
        return [pscustomobject]$evaluation
    }

    $evaluation.Exists = $true
    $evaluation.Content = Get-Content $fullPath -Raw
    $evaluation.SanitizedContent = Strip-FencedCodeBlocks $evaluation.Content
    $evaluation.LineCount = (Get-Content $fullPath).Count
    $evaluation.HeadingCount = Get-HeadingCount $evaluation.Content
    $evaluation.TableCount = Get-TableCount $evaluation.Content
    $evaluation.CodeBlockCount = [int](Get-CodeBlockCount $evaluation.Content)
    $evaluation.BulletCount = Get-BulletLineCount $evaluation.Content
    $evaluation.LongParagraphs = Get-LongParagraphBlockCount $evaluation.SanitizedContent

    $msg = "Found $FileName"
    Pass $msg
    $msg = "$FileName line count: $($evaluation.LineCount)"
    Pass $msg

    foreach ($heading in $RequiredHeadings[$FileName]) {
        if (Test-RequiredHeading -Content $evaluation.Content -Heading $heading) {
            $evaluation.RequiredFound += $heading
            $msg = "$FileName contains '$heading'"
            Pass $msg
        }
        else {
            $evaluation.MissingHeadings += $heading
            $msg = "$FileName missing '$heading'"
            Fail $msg
        }
    }

    $evaluation.PlaceholderHits = Get-PatternMatches -Content $evaluation.Content -Patterns $PlaceholderPatterns
    if ($evaluation.PlaceholderHits.Count -eq 0) {
        $msg = "$FileName has no unresolved placeholders"
        Pass $msg
    }
    else {
        $msg = "$FileName contains placeholder-like content: $($evaluation.PlaceholderHits.Count)"
        Warn $msg
    }

    $evaluation.RepoPathErrors = Get-RepoLocalPathErrors -Content $evaluation.Content -RootPath $RootPath
    if ($evaluation.RepoPathErrors.Count -eq 0) {
        $msg = "$FileName has no broken repo-local path references"
        Pass $msg
    }
    else {
        $msg = "$FileName contains broken repo-local path references: $($evaluation.RepoPathErrors -join ', ')"
        Warn $msg
    }

    $evaluation.VagueHits = Get-PatternMatches -Content $evaluation.SanitizedContent -Patterns $VaguePatterns
    if ($evaluation.VagueHits.Count -eq 0) {
        $msg = "$FileName avoids vague rule phrasing"
        Pass $msg
    }
    else {
        $msg = "$FileName contains vague phrasing: $($evaluation.VagueHits -join ', ')"
        Warn $msg
    }

    $evaluation.HardcodedHits = Get-HardcodedSkillHits -Content $evaluation.Content
    if ($evaluation.HardcodedHits.Count -eq 0) {
        $msg = "$FileName has no positive-context hardcoded skill invocations"
        Pass $msg
    }
    else {
        $msg = "$FileName contains literal skill invocations: $($evaluation.HardcodedHits -join ', ')"
        Warn $msg
    }

    if ($evaluation.TableCount -gt 0) {
        $msg = "$FileName includes tabular structure"
        Pass $msg
    }
    else {
        $msg = "$FileName has no markdown tables"
        Warn $msg
    }

    if ($evaluation.CodeBlockCount -gt 0) {
        $msg = "$FileName includes fenced code blocks"
        Pass $msg
    }
    else {
        $msg = "$FileName has no fenced code blocks"
        Warn $msg
    }

    if ($evaluation.LongParagraphs -eq 0) {
        $msg = "$FileName avoids long wall-of-text paragraphs"
        Pass $msg
    }
    else {
        $msg = "$FileName has long paragraph blocks: $($evaluation.LongParagraphs)"
        Warn $msg
    }

    $completeness = $evaluation.RequiredFound.Count * 2

    $accuracy = 10
    $accuracy -= [Math]::Min(6, $evaluation.PlaceholderHits.Count * 2)
    $accuracy -= [Math]::Min(4, $evaluation.RepoPathErrors.Count)
    if ($accuracy -lt 0) { $accuracy = 0 }

    $specificity = 10
    if ($evaluation.TableCount -eq 0) { $specificity -= 2 }
    if ($evaluation.CodeBlockCount -eq 0) { $specificity -= 2 }
    if ($evaluation.Content -notmatch '(?i)\bexample\b|for example|\bgood\b|\bbad\b') { $specificity -= 2 }
    $specificity -= [Math]::Min(4, $evaluation.VagueHits.Count * 2)
    if ($specificity -lt 0) { $specificity = 0 }

    $scannability = 10
    if ($evaluation.HeadingCount -lt 5) { $scannability -= 2 }
    if ($evaluation.BulletCount -lt 5) { $scannability -= 2 }
    if ($evaluation.TableCount -eq 0) { $scannability -= 1 }
    $scannability -= [Math]::Min(5, $evaluation.LongParagraphs * 2)
    if ($scannability -lt 0) { $scannability = 0 }

    $evaluation.Scores.Completeness = $completeness
    $evaluation.Scores.Accuracy = $accuracy
    $evaluation.Scores.Specificity = $specificity
    $evaluation.Scores.Scannability = $scannability

    return [pscustomobject]$evaluation
}

function Finalize-ConsistencyScores([object]$Primary, [object]$Secondary) {
    if (-not $Primary.Exists) {
        return
    }

    $consistency = 10
    if ($Primary.HardcodedHits.Count -gt 0) {
        $consistency -= [Math]::Min(6, $Primary.HardcodedHits.Count * 3)
    }

    if ($Secondary.Exists) {
        $primaryLines = Get-MeaningfulLines $Primary.SanitizedContent
        $secondaryLines = Get-MeaningfulLines $Secondary.SanitizedContent
        $commonLines = Compare-Object -ReferenceObject $primaryLines -DifferenceObject $secondaryLines -IncludeEqual |
            Where-Object { $_.SideIndicator -eq '==' } |
            Select-Object -ExpandProperty InputObject

        $Primary.DuplicationCount = @($commonLines).Count

        if ($Primary.DuplicationCount -gt 12) {
            $consistency -= 4
        }
        elseif ($Primary.DuplicationCount -gt 6) {
            $consistency -= 2
        }
    }

    if ($consistency -lt 0) { $consistency = 0 }

    $Primary.Scores.Consistency = $consistency
    $Primary.Scores.Total =
        $Primary.Scores.Completeness +
        $Primary.Scores.Accuracy +
        $Primary.Scores.Specificity +
        $Primary.Scores.Scannability +
        $Primary.Scores.Consistency
}

function Write-Scorecard([object]$Evaluation, [int]$EffectiveThreshold) {
    Write-Host ""
    Write-Host "$($Evaluation.FileName) Scorecard:" -ForegroundColor White
    Write-Host ("  Completeness: {0}/10" -f $Evaluation.Scores.Completeness)
    Write-Host ("  Accuracy:     {0}/10" -f $Evaluation.Scores.Accuracy)
    Write-Host ("  Specificity:  {0}/10" -f $Evaluation.Scores.Specificity)
    Write-Host ("  Scannability: {0}/10" -f $Evaluation.Scores.Scannability)
    Write-Host ("  Consistency:  {0}/10" -f $Evaluation.Scores.Consistency)
    Write-Host ("  Total:        {0}/50" -f $Evaluation.Scores.Total)

    if ($Evaluation.DuplicationCount -gt 12) {
        $msg = "$($Evaluation.FileName) duplicates too much content across files ($($Evaluation.DuplicationCount) common lines)"
        Warn $msg
    }
    elseif ($Evaluation.DuplicationCount -gt 6) {
        $msg = "$($Evaluation.FileName) has moderate cross-file duplication ($($Evaluation.DuplicationCount) common lines)"
        Warn $msg
    }
    elseif ($Evaluation.Exists) {
        $msg = "$($Evaluation.FileName) keeps cross-file duplication low ($($Evaluation.DuplicationCount) common lines)"
        Pass $msg
    }

    if ($Evaluation.Scores.Total -ge $EffectiveThreshold) {
        $msg = "$($Evaluation.FileName) meets threshold $EffectiveThreshold/50"
        Pass $msg
    }
    else {
        $msg = "$($Evaluation.FileName) fails threshold $EffectiveThreshold/50"
        Fail $msg
    }
}

$projectRoot = (Resolve-Path $Path).Path
$effectiveThreshold = Get-EffectiveThreshold -RootPath $projectRoot -CliThreshold $Threshold -StrictMode:$Strict

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " AI Project Rules Generator - Output Validation" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Project:   $projectRoot"
Write-Host "  Threshold: $effectiveThreshold/50"
Write-Host ("  Strict:    {0}" -f ($(if ($Strict) { "on" } else { "off" })))

$cursorEvaluation = New-FileEvaluation -FileName ".cursorrules" -RootPath $projectRoot
$agentsEvaluation = New-FileEvaluation -FileName "AGENTS.md" -RootPath $projectRoot

Finalize-ConsistencyScores -Primary $cursorEvaluation -Secondary $agentsEvaluation
Finalize-ConsistencyScores -Primary $agentsEvaluation -Secondary $cursorEvaluation

Write-Scorecard -Evaluation $cursorEvaluation -EffectiveThreshold $effectiveThreshold
Write-Scorecard -Evaluation $agentsEvaluation -EffectiveThreshold $effectiveThreshold

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Validation Summary" -ForegroundColor White
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ("  Raw checks passed: {0}/{1}" -f $script:PassedChecks, $script:TotalChecks)
Write-Host ("  Warnings:          {0}" -f $script:Warnings.Count)
Write-Host ("  Errors:            {0}" -f $script:Errors.Count)
Write-Host ("  .cursorrules:      {0}/50" -f $cursorEvaluation.Scores.Total)
Write-Host ("  AGENTS.md:         {0}/50" -f $agentsEvaluation.Scores.Total)
Write-Host ""

if ($script:Errors.Count -eq 0) {
    Write-Host "  Result: PASS" -ForegroundColor Green
}
else {
    Write-Host "  Result: FAIL" -ForegroundColor Red
    foreach ($errorMessage in $script:Errors) {
        Write-Host "    - $errorMessage" -ForegroundColor Red
    }
}

if ($script:Warnings.Count -gt 0) {
    Write-Host ""
    Write-Host "  Warning Details:" -ForegroundColor Yellow
    foreach ($warningMessage in $script:Warnings) {
        Write-Host "    - $warningMessage" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan

if ($script:Errors.Count -gt 0) {
    exit 1
}
