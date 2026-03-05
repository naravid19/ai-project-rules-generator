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
    Write-Host "Note: Skill sources (.agent/skills/, .agent/awesome-claude-skills/) were NOT removed." -ForegroundColor DarkGray
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
New-Item -ItemType Directory -Force -Path ".agent/skills" | Out-Null

Write-Host "Downloading workflow..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "$RepoRaw/workflows/create-project-rules.md" -OutFile $WorkflowFile

$version = Get-WorkflowVersion -Path $WorkflowFile
Write-Host "✅ Workflow installed at $WorkflowFile (version: $version)" -ForegroundColor Green
Write-Host ""

# ─── Skill Source Selection ──────────────────────────────────────────────────
if ($SkillSource) {
    # Direct skill source via parameter
    switch ($SkillSource.ToLower()) {
        "antigravity" {
            Update-OrCloneRepo -RepoUrl "https://github.com/sickn33/antigravity-awesome-skills.git" -TargetPath ".agent/skills" -Label "antigravity-awesome-skills"
        }
        "claude" {
            Update-OrCloneRepo -RepoUrl "https://github.com/ComposioHQ/awesome-claude-skills.git" -TargetPath ".agent/awesome-claude-skills" -Label "awesome-claude-skills"
        }
        "anthropic" {
            Update-OrCloneRepo -RepoUrl "https://github.com/anthropics/skills.git" -TargetPath ".agent/anthropic-skills" -Label "anthropic-skills"
        }
        "techleads" {
            Update-OrCloneRepo -RepoUrl "https://github.com/tech-leads-club/agent-skills.git" -TargetPath ".agent/agent-skills" -Label "agent-skills"
        }
        "jeffallan" {
            Update-OrCloneRepo -RepoUrl "https://github.com/Jeffallan/claude-skills.git" -TargetPath ".agent/claude-skills" -Label "claude-skills"
        }
        "all" {
            Update-OrCloneRepo -RepoUrl "https://github.com/sickn33/antigravity-awesome-skills.git" -TargetPath ".agent/skills" -Label "antigravity-awesome-skills"
            Update-OrCloneRepo -RepoUrl "https://github.com/ComposioHQ/awesome-claude-skills.git" -TargetPath ".agent/awesome-claude-skills" -Label "awesome-claude-skills"
            Update-OrCloneRepo -RepoUrl "https://github.com/anthropics/skills.git" -TargetPath ".agent/anthropic-skills" -Label "anthropic-skills"
            Update-OrCloneRepo -RepoUrl "https://github.com/tech-leads-club/agent-skills.git" -TargetPath ".agent/agent-skills" -Label "agent-skills"
            Update-OrCloneRepo -RepoUrl "https://github.com/Jeffallan/claude-skills.git" -TargetPath ".agent/claude-skills" -Label "claude-skills"
        }
        default {
            Write-Host "Unknown skill source: $SkillSource. Options: antigravity, claude, anthropic, techleads, jeffallan, all" -ForegroundColor Red
        }
    }
}
elseif ($NonInteractive) {
    Write-Host "Non-interactive mode: skipping skill source selection." -ForegroundColor DarkGray
    Write-Host "Use -SkillSource <name> to install skill sources." -ForegroundColor DarkGray
}
else {
    Write-Host "Recommended skill sources (optional):" -ForegroundColor Cyan
    Write-Host "  1) antigravity-awesome-skills  (CATALOG format, 968+ skills)"
    Write-Host "  2) awesome-claude-skills       (FOLDER format, 30+ skills)"
    Write-Host "  3) anthropic-skills            (FOLDER format, 50+ official Anthropic skills)"
    Write-Host "  4) agent-skills                (FOLDER format, curated & human-reviewed)"
    Write-Host "  5) claude-skills               (FOLDER format, 66 full-stack skills)"
    Write-Host "  6) All of the above"
    Write-Host "  7) Skip (add your own later)"
    Write-Host ""
    $choice = Read-Host "Choose [1-7]"

    switch ($choice) {
        "1" {
            Update-OrCloneRepo -RepoUrl "https://github.com/sickn33/antigravity-awesome-skills.git" -TargetPath ".agent/skills" -Label "antigravity-awesome-skills"
        }
        "2" {
            Update-OrCloneRepo -RepoUrl "https://github.com/ComposioHQ/awesome-claude-skills.git" -TargetPath ".agent/awesome-claude-skills" -Label "awesome-claude-skills"
        }
        "3" {
            Update-OrCloneRepo -RepoUrl "https://github.com/anthropics/skills.git" -TargetPath ".agent/anthropic-skills" -Label "anthropic-skills"
        }
        "4" {
            Update-OrCloneRepo -RepoUrl "https://github.com/tech-leads-club/agent-skills.git" -TargetPath ".agent/agent-skills" -Label "agent-skills"
        }
        "5" {
            Update-OrCloneRepo -RepoUrl "https://github.com/Jeffallan/claude-skills.git" -TargetPath ".agent/claude-skills" -Label "claude-skills"
        }
        "6" {
            Update-OrCloneRepo -RepoUrl "https://github.com/sickn33/antigravity-awesome-skills.git" -TargetPath ".agent/skills" -Label "antigravity-awesome-skills"
            Update-OrCloneRepo -RepoUrl "https://github.com/ComposioHQ/awesome-claude-skills.git" -TargetPath ".agent/awesome-claude-skills" -Label "awesome-claude-skills"
            Update-OrCloneRepo -RepoUrl "https://github.com/anthropics/skills.git" -TargetPath ".agent/anthropic-skills" -Label "anthropic-skills"
            Update-OrCloneRepo -RepoUrl "https://github.com/tech-leads-club/agent-skills.git" -TargetPath ".agent/agent-skills" -Label "agent-skills"
            Update-OrCloneRepo -RepoUrl "https://github.com/Jeffallan/claude-skills.git" -TargetPath ".agent/claude-skills" -Label "claude-skills"
        }
        "7" {
            Write-Host "Skipping skill source installation." -ForegroundColor DarkGray
        }
        default {
            Write-Host "Invalid choice, skipping skill source installation." -ForegroundColor DarkGray
        }
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
Write-Host "  Verbose:     .\setup.ps1 -Verbose" -ForegroundColor Blue
Write-Host ""
Write-Host "Docs: https://github.com/naravid19/ai-project-rules-generator" -ForegroundColor Blue
Write-Host "===============================================" -ForegroundColor Cyan
