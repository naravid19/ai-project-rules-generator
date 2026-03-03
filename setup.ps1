# =============================================================================
# Setup & Update - AI Project Rules Generator
# =============================================================================
# Install:  irm <raw-url>/setup.ps1 | iex
# Update:   .\setup.ps1 -Update
# =============================================================================

param(
    [switch]$Update
)

$ErrorActionPreference = "Stop"
$RepoRaw = "https://raw.githubusercontent.com/naravid19/ai-project-rules-generator/main"
$WorkflowFile = ".agent/workflows/create-project-rules.md"

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

function Clone-OrUpdateRepo {
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

if ($Update) {
    Write-Host "AI Project Rules Generator - Update" -ForegroundColor Cyan
    Write-Host "===================================" -ForegroundColor Cyan
    Write-Host ""

    if (-not (Test-Path $WorkflowFile)) {
        Write-Host "Workflow not found at $WorkflowFile" -ForegroundColor Red
        Write-Host "Run without -Update to install first."
        exit 1
    }

    Copy-Item $WorkflowFile "$WorkflowFile.backup" -Force
    Write-Host "Backed up current workflow to $WorkflowFile.backup" -ForegroundColor Yellow

    Write-Host "Downloading latest workflow..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "$RepoRaw/workflows/create-project-rules.md" -OutFile $WorkflowFile

    $version = Get-WorkflowVersion -Path $WorkflowFile
    Write-Host "Workflow updated successfully." -ForegroundColor Green
    Write-Host "Current version: $version"
    Write-Host "Backup saved at: $WorkflowFile.backup"
    Write-Host ""
    Write-Host "Tip: Your .cursorrules and AGENTS.md are NOT affected." -ForegroundColor DarkGray
    Write-Host "Re-run /create-project-rules to regenerate with latest workflow."
    Write-Host "===================================" -ForegroundColor Cyan
    exit 0
}

Write-Host "AI Project Rules Generator - Quick Start Setup" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Creating .agent/ directory structure..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path ".agent/workflows" | Out-Null
New-Item -ItemType Directory -Force -Path ".agent/skills" | Out-Null

Write-Host "Downloading workflow..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "$RepoRaw/workflows/create-project-rules.md" -OutFile $WorkflowFile
Write-Host "Workflow installed at $WorkflowFile" -ForegroundColor Green
Write-Host ""

Write-Host "Recommended skill sources (optional):" -ForegroundColor Cyan
Write-Host "  1) antigravity-awesome-skills (CATALOG format)"
Write-Host "  2) awesome-claude-skills (README format)"
Write-Host "  3) All of the above"
Write-Host "  4) Skip (add your own later)"
Write-Host ""
$choice = Read-Host "Choose [1-4]"

switch ($choice) {
    "1" {
        Clone-OrUpdateRepo -RepoUrl "https://github.com/sickn33/antigravity-awesome-skills.git" -TargetPath ".agent/skills" -Label "antigravity-awesome-skills"
    }
    "2" {
        Clone-OrUpdateRepo -RepoUrl "https://github.com/ComposioHQ/awesome-claude-skills.git" -TargetPath ".agent/awesome-claude-skills" -Label "awesome-claude-skills"
    }
    "3" {
        Clone-OrUpdateRepo -RepoUrl "https://github.com/sickn33/antigravity-awesome-skills.git" -TargetPath ".agent/skills" -Label "antigravity-awesome-skills"
        Clone-OrUpdateRepo -RepoUrl "https://github.com/ComposioHQ/awesome-claude-skills.git" -TargetPath ".agent/awesome-claude-skills" -Label "awesome-claude-skills"
    }
    "4" {
        Write-Host "Skipping skill source installation." -ForegroundColor DarkGray
    }
    default {
        Write-Host "Invalid choice, skipping skill source installation." -ForegroundColor DarkGray
    }
}

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "Setup complete." -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1) Open your project in your AI assistant"
Write-Host "  2) Run: /create-project-rules"
Write-Host "  3) Get tailored .cursorrules + AGENTS.md"
Write-Host ""
Write-Host "Docs: https://github.com/naravid19/ai-project-rules-generator" -ForegroundColor Blue
Write-Host "Update later: .\setup.ps1 -Update" -ForegroundColor Blue
Write-Host "===============================================" -ForegroundColor Cyan
