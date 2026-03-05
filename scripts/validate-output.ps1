# =============================================================================
# Validate Output — AI Project Rules Generator
# =============================================================================
# Validates generated .cursorrules and AGENTS.md files for quality.
# Usage: .\scripts\validate-output.ps1 [-Path <project-root>] [-Strict]
# =============================================================================

param(
    [string]$Path = ".",
    [switch]$Strict,
    [int]$Threshold = 38
)

$ErrorActionPreference = "Continue"

# ─── Counters ────────────────────────────────────────────────────────────────
$script:TotalChecks = 0
$script:PassedChecks = 0
$script:Warnings = @()
$script:Errors = @()

function Pass([string]$msg) {
    $script:PassedChecks++
    $script:TotalChecks++
    Write-Host "  ✅ $msg" -ForegroundColor Green
}

function Fail([string]$msg) {
    $script:TotalChecks++
    $script:Errors += $msg
    Write-Host "  ❌ $msg" -ForegroundColor Red
}

function Warn([string]$msg) {
    $script:Warnings += $msg
    Write-Host "  ⚠️  $msg" -ForegroundColor Yellow
}

function Test-FileExists([string]$relativePath) {
    $fullPath = Join-Path $Path $relativePath
    if (Test-Path $fullPath) {
        Pass "Found $relativePath"
        return $true
    }
    else {
        Fail "Missing $relativePath"
        return $false
    }
}

function Test-SectionExists([string]$file, [string]$section) {
    $fullPath = Join-Path $Path $file
    if (Test-Path $fullPath) {
        $content = Get-Content $fullPath -Raw -ErrorAction SilentlyContinue
        if ($content -match [regex]::Escape($section)) {
            Pass "$file contains '$section'"
            return $true
        }
        else {
            Fail "$file missing section '$section'"
            return $false
        }
    }
    return $false
}

function Test-NoHardcodedSkills([string]$file) {
    $fullPath = Join-Path $Path $file
    if (Test-Path $fullPath) {
        $content = Get-Content $fullPath -Raw -ErrorAction SilentlyContinue
        if ($content -match '@[a-z]+-[a-z]+') {
            Fail "$file contains hardcoded skill names (@skill-name pattern)"
            return $false
        }
        else {
            Pass "$file has no hardcoded skill names"
            return $true
        }
    }
    return $true
}

function Get-LineCount([string]$file) {
    $fullPath = Join-Path $Path $file
    if (Test-Path $fullPath) {
        return (Get-Content $fullPath).Count
    }
    return 0
}

# ─── Main Validation ─────────────────────────────────────────────────────────
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   AI Project Rules Generator — Output Validation        ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Project: $Path"
Write-Host "  Threshold: $Threshold/50"
Write-Host ""

# ─── Check 1: File Existence ─────────────────────────────────────────────────
Write-Host "📁 File Existence:" -ForegroundColor White
$hasCursorRules = Test-FileExists ".cursorrules"
$hasAgents = Test-FileExists "AGENTS.md"
Write-Host ""

# ─── Check 2: .cursorrules Structure ─────────────────────────────────────────
if ($hasCursorRules) {
    Write-Host "📋 .cursorrules Structure:" -ForegroundColor White
    Test-SectionExists ".cursorrules" "Project Identity" | Out-Null
    Test-SectionExists ".cursorrules" "Coding Standards" | Out-Null
    Test-SectionExists ".cursorrules" "Critical Rules" | Out-Null
    Test-SectionExists ".cursorrules" "Code Smells" | Out-Null

    $lines = Get-LineCount ".cursorrules"
    if ($lines -ge 100) {
        Pass ".cursorrules has sufficient content ($lines lines)"
    }
    elseif ($lines -ge 50) {
        Warn ".cursorrules is short ($lines lines, recommended: 150-400)"
    }
    else {
        Fail ".cursorrules is too short ($lines lines, minimum: 100)"
    }

    Test-NoHardcodedSkills ".cursorrules" | Out-Null
    Write-Host ""
}

# ─── Check 3: AGENTS.md Structure ────────────────────────────────────────────
if ($hasAgents) {
    Write-Host "📋 AGENTS.md Structure:" -ForegroundColor White
    Test-SectionExists "AGENTS.md" "Quick Context" | Out-Null
    Test-SectionExists "AGENTS.md" "Available Skills" | Out-Null
    Test-SectionExists "AGENTS.md" "Constraints" | Out-Null

    $lines = Get-LineCount "AGENTS.md"
    if ($lines -ge 80) {
        Pass "AGENTS.md has sufficient content ($lines lines)"
    }
    elseif ($lines -ge 40) {
        Warn "AGENTS.md is short ($lines lines, recommended: 100-250)"
    }
    else {
        Fail "AGENTS.md is too short ($lines lines, minimum: 80)"
    }

    Test-NoHardcodedSkills "AGENTS.md" | Out-Null
    Write-Host ""
}

# ─── Check 4: Content Smells ─────────────────────────────────────────────────
Write-Host "🔍 Content Smell Detection:" -ForegroundColor White

foreach ($file in @(".cursorrules", "AGENTS.md")) {
    $fullPath = Join-Path $Path $file
    if (Test-Path $fullPath) {
        $content = Get-Content $fullPath -Raw -ErrorAction SilentlyContinue

        # Vague rules check
        if ($content -match 'write good code|write clean code|follow best practices') {
            Warn "$file contains vague rules (e.g., 'write good code')"
        }
        else {
            Pass "$file has no vague rules"
        }
    }
}
Write-Host ""

# ─── Check 5: Consistency ────────────────────────────────────────────────────
if ($hasCursorRules -and $hasAgents) {
    Write-Host "🔗 Cross-File Consistency:" -ForegroundColor White
    Pass "Both files exist for consistency check"
    Write-Host ""
}

# ─── Summary ─────────────────────────────────────────────────────────────────
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Validation Summary:" -ForegroundColor White
Write-Host "   Checks: $script:PassedChecks/$script:TotalChecks passed"
Write-Host "   Warnings: $($script:Warnings.Count)"
Write-Host "   Errors: $($script:Errors.Count)"
Write-Host ""

if ($script:Errors.Count -eq 0) {
    Write-Host "  ✅ PASSED — All checks passed!" -ForegroundColor Green
}
else {
    Write-Host "  ❌ FAILED — $($script:Errors.Count) error(s) found:" -ForegroundColor Red
    foreach ($err in $script:Errors) {
        Write-Host "     • $err" -ForegroundColor Red
    }
}

if ($script:Warnings.Count -gt 0) {
    Write-Host ""
    Write-Host "  ⚠️  Warnings:" -ForegroundColor Yellow
    foreach ($w in $script:Warnings) {
        Write-Host "     • $w" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

if ($script:Errors.Count -gt 0) {
    exit 1
}
