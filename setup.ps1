# =============================================================================
# Setup & Update - AI Project Rules Generator
# =============================================================================
# Install:  irm <raw-url>/setup.ps1 | iex
# Update:   .\setup.ps1 -Update
# =============================================================================

param(
    [switch]$Update,
    [switch]$NonInteractive,
    [switch]$Verbose,
    [string]$SkillSource,
    [string]$SkillRoot = ".agent",
    [switch]$Uninstall
)

$ErrorActionPreference = "Stop"
$RepoRaw = "https://raw.githubusercontent.com/naravid19/ai-project-rules-generator/main"
$WorkflowFile = ".agent/workflows/create-project-rules.md"

function Write-Log([string]$msg) {
    if ($Verbose) {
        Write-Host "[DEBUG] $msg" -ForegroundColor DarkGray
    }
}

function Get-WorkflowVersion {
    param([string]$Path)

    $version = "unknown"
    $versionRows = Select-String -Path $Path -Pattern '^\|\s*\d+\.\d+\s*\|' | ForEach-Object { $_.Line }
    if ($versionRows) {
        $lastRow = $versionRows[-1]
        if ($lastRow -match '^\|\s*(\d+\.\d+)\s*\|') {
            $version = "v$($Matches[1])"
        }
    }
    return $version
}

function Update-OrCloneRepo {
    param(
        [string]$RepoUrl,
        [string]$TargetPath,
        [string]$Label
    )

    if (Test-Path "$TargetPath/.git") {
        Write-Host "Updating $Label..." -ForegroundColor Yellow
        git -C $TargetPath pull --ff-only
        return
    }

    if (Test-Path $TargetPath) {
        $items = Get-ChildItem -Force -Path $TargetPath -ErrorAction SilentlyContinue
        if ($items.Count -gt 0) {
            Write-Host "Skip ${Label}: target exists and is not an empty git repo ($TargetPath)." -ForegroundColor DarkGray
            return
        }
    }

    Write-Host "Cloning $Label..." -ForegroundColor Yellow
    git clone --depth 1 $RepoUrl $TargetPath
}

function Install-Skill {
    param([string]$Key)

    switch ($Key) {
        "antigravity" {
            Update-OrCloneRepo -RepoUrl "https://github.com/sickn33/antigravity-awesome-skills.git" -TargetPath (Join-Path $SkillRoot "skills") -Label "sickn33/antigravity-awesome-skills"
        }
        "claude" {
            Update-OrCloneRepo -RepoUrl "https://github.com/ComposioHQ/awesome-claude-skills.git" -TargetPath (Join-Path $SkillRoot "awesome-claude-skills") -Label "ComposioHQ/awesome-claude-skills"
        }
        "anthropic" {
            Update-OrCloneRepo -RepoUrl "https://github.com/anthropics/skills.git" -TargetPath (Join-Path $SkillRoot "anthropic-skills") -Label "anthropics/skills"
        }
        "techleads" {
            Update-OrCloneRepo -RepoUrl "https://github.com/tech-leads-club/agent-skills.git" -TargetPath (Join-Path $SkillRoot "techleads-agent-skills") -Label "tech-leads-club/agent-skills"
        }
        "jeffallan" {
            Update-OrCloneRepo -RepoUrl "https://github.com/Jeffallan/claude-skills.git" -TargetPath (Join-Path $SkillRoot "jeffallan-claude-skills") -Label "Jeffallan/claude-skills"
        }
        "ui-ux-pro-max" {
            Update-OrCloneRepo -RepoUrl "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git" -TargetPath (Join-Path $SkillRoot "ui-ux-pro-max-skill") -Label "nextlevelbuilder/ui-ux-pro-max-skill"
        }
        "othmanadi" {
            Update-OrCloneRepo -RepoUrl "https://github.com/OthmanAdi/planning-with-files.git" -TargetPath (Join-Path $SkillRoot "othman-planning-with-files") -Label "OthmanAdi/planning-with-files"
        }
        "all" {
            $keys = @("antigravity", "claude", "anthropic", "techleads", "jeffallan", "ui-ux-pro-max", "othmanadi")
            foreach ($k in $keys) { Install-Skill -Key $k }
        }
        default {
            Write-Host "Unknown skill source: $Key. Options: antigravity, claude, anthropic, techleads, jeffallan, ui-ux-pro-max, othmanadi, all" -ForegroundColor Red
        }
    }
}

# ─── Prerequisite Check ──────────────────────────────────────────────────────
function Test-Prerequisites {
    # Check Git
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Host "❌ Git is required but not found." -ForegroundColor Red
        Write-Host "   Install from: https://git-scm.com/downloads" -ForegroundColor Yellow
        Write-Host "   Or via winget: winget install Git.Git" -ForegroundColor Yellow
        exit 1
    }
    Write-Log "Git found: $(git --version)"

    # Check internet connectivity
    try {
        $null = Invoke-WebRequest -Uri "https://github.com" -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
        Write-Log "Internet connectivity OK"
    }
    catch {
        Write-Host "❌ Cannot reach GitHub. Check your internet connection." -ForegroundColor Red
        exit 1
    }
}

# ─── Uninstall ───────────────────────────────────────────────────────────────
if ($Uninstall) {
    Write-Host "AI Project Rules Generator - Uninstall" -ForegroundColor Cyan
    Write-Host "=======================================" -ForegroundColor Cyan
    Write-Host ""

    $filesToRemove = @(
        $WorkflowFile,
        "$WorkflowFile.backup"
    )

    foreach ($file in $filesToRemove) {
        if (Test-Path $file) {
            Remove-Item $file -Force
            Write-Host "  Removed: $file" -ForegroundColor Yellow
        }
    }

    # Check if .agent/workflows is empty
    if ((Test-Path ".agent/workflows") -and
        (Get-ChildItem ".agent/workflows" -ErrorAction SilentlyContinue).Count -eq 0) {
        Remove-Item ".agent/workflows" -Force
        Write-Host "  Removed empty: .agent/workflows/" -ForegroundColor Yellow
    }

    Write-Host ""
    Write-Host "Uninstall complete." -ForegroundColor Green
    Write-Host "Note: Skill sources (.agent/skills/, shared SkillRoot paths, etc.) were NOT removed." -ForegroundColor DarkGray
    Write-Host "      Remove them manually if desired." -ForegroundColor DarkGray
    Write-Host "=======================================" -ForegroundColor Cyan
    exit 0
}

# ─── Update ──────────────────────────────────────────────────────────────────
if ($Update) {
    Write-Host "AI Project Rules Generator - Update" -ForegroundColor Cyan
    Write-Host "===================================" -ForegroundColor Cyan
    Write-Host ""

    Test-Prerequisites

    if (-not (Test-Path $WorkflowFile)) {
        Write-Host "❌ Workflow not found at $WorkflowFile" -ForegroundColor Red
        Write-Host "Run without -Update to install first."
        exit 1
    }

    Copy-Item $WorkflowFile "$WorkflowFile.backup" -Force
    Write-Host "Backed up current workflow to $WorkflowFile.backup" -ForegroundColor Yellow

    Write-Host "Downloading latest workflow..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "$RepoRaw/workflows/create-project-rules.md" -OutFile $WorkflowFile

    $version = Get-WorkflowVersion -Path $WorkflowFile
    Write-Host "✅ Workflow updated successfully." -ForegroundColor Green
    Write-Host "Current version: $version"
    Write-Host "Backup saved at: $WorkflowFile.backup"
    Write-Host ""
    Write-Host "Tip: Your .cursorrules and AGENTS.md are NOT affected." -ForegroundColor DarkGray
    Write-Host "Re-run /create-project-rules to regenerate with latest workflow."
    Write-Host "===================================" -ForegroundColor Cyan
    exit 0
}

# ─── Install ─────────────────────────────────────────────────────────────────
Write-Host "AI Project Rules Generator - Quick Start Setup" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

Test-Prerequisites

Write-Host "Creating .agent/ directory structure..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path ".agent/workflows" | Out-Null
New-Item -ItemType Directory -Force -Path $SkillRoot | Out-Null

if ($SkillRoot -ne ".agent") {
    Write-Host "Using shared skill root: $SkillRoot" -ForegroundColor DarkGray
    Write-Host "Keeping workflow local at $WorkflowFile" -ForegroundColor DarkGray
}

Write-Host "Downloading workflow..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "$RepoRaw/workflows/create-project-rules.md" -OutFile $WorkflowFile

$version = Get-WorkflowVersion -Path $WorkflowFile
Write-Host "✅ Workflow installed at $WorkflowFile (version: $version)" -ForegroundColor Green
Write-Host ""

# ─── Skill Source Selection ──────────────────────────────────────────────────
if ($SkillSource) {
    # Direct skill source via parameter
    Install-Skill -Key $SkillSource.ToLower()
}
elseif ($NonInteractive) {
    Write-Host "Non-interactive mode: skipping skill source selection." -ForegroundColor DarkGray
    Write-Host "Use -SkillSource <name> to install skill sources." -ForegroundColor DarkGray
    Write-Host "Use -SkillRoot <path> to install sources into a shared skill root." -ForegroundColor DarkGray
}
else {
    Write-Host "Recommended skill sources (optional):" -ForegroundColor Cyan
    Write-Host "Install root for skill sources: $SkillRoot" -ForegroundColor DarkGray
    Write-Host "  1) sickn33 / antigravity-awesome-skills  (CATALOG, 968+ skills)"
    Write-Host "  2) ComposioHQ / awesome-claude-skills    (FOLDER, 30+ skills)"
    Write-Host "  3) anthropics / skills                   (FOLDER, 50+ official Anthropic skills)"
    Write-Host "  4) tech-leads-club / agent-skills        (FOLDER, curated & human-reviewed)"
    Write-Host "  5) Jeffallan / claude-skills             (FOLDER, 66 full-stack skills)"
    Write-Host "  6) nextlevelbuilder / ui-ux-pro-max      (WORKFLOW, UI/UX design intel)"
    Write-Host "  7) OthmanAdi / planning-with-files       (FOLDER, Manus-style persistence)"
    Write-Host "  8) All of the above"
    Write-Host "  9) Skip (add your own later)"
    Write-Host ""
    $choice = Read-Host "Choose [1-9]"

    switch ($choice) {
        "1" { Install-Skill -Key "antigravity" }
        "2" { Install-Skill -Key "claude" }
        "3" { Install-Skill -Key "anthropic" }
        "4" { Install-Skill -Key "techleads" }
        "5" { Install-Skill -Key "jeffallan" }
        "6" { Install-Skill -Key "ui-ux-pro-max" }
        "7" { Install-Skill -Key "othmanadi" }
        "8" { Install-Skill -Key "all" }
        "9" { Write-Host "Skipping skill source installation." -ForegroundColor DarkGray }
        default { Write-Host "Invalid choice, skipping skill source installation." -ForegroundColor DarkGray }
    }
}

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "✅ Setup complete." -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1) Open your project in your AI assistant"
Write-Host "  2) Run: /create-project-rules"
Write-Host "  3) Get tailored .cursorrules + AGENTS.md"
Write-Host ""
Write-Host "Options:"
Write-Host "  Update:      .\setup.ps1 -Update" -ForegroundColor Blue
Write-Host "  Uninstall:   .\setup.ps1 -Uninstall" -ForegroundColor Blue
Write-Host "  CI/CD mode:  .\setup.ps1 -NonInteractive -SkillSource all" -ForegroundColor Blue
Write-Host "  Shared root: .\setup.ps1 -SkillSource all -SkillRoot C:\Shared\.agent" -ForegroundColor Blue
Write-Host "  Verbose:     .\setup.ps1 -Verbose" -ForegroundColor Blue
Write-Host ""
Write-Host "Docs: https://github.com/naravid19/ai-project-rules-generator" -ForegroundColor Blue
Write-Host "===============================================" -ForegroundColor Cyan
