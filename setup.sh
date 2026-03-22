#!/usr/bin/env bash
# =============================================================================
# Setup & Update - AI Project Rules Generator
# =============================================================================
# Install:  curl -sL <raw-url>/setup.sh | bash
# Update:   ./setup.sh --update
# =============================================================================

set -euo pipefail

REPO_RAW="https://raw.githubusercontent.com/naravid19/ai-project-rules-generator/main"
WORKFLOW_FILE=".agent/workflows/create-project-rules.md"
VERBOSE=false
NON_INTERACTIVE=false
SKILL_SOURCE=""
SKILL_ROOT=".agent"
UNINSTALL=false

# ─── Parse Arguments ─────────────────────────────────────────────────────────
ACTION="install"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --update|-u) ACTION="update"; shift ;;
    --uninstall) UNINSTALL=true; shift ;;
    --non-interactive) NON_INTERACTIVE=true; shift ;;
    --verbose|-v) VERBOSE=true; shift ;;
    --skill-source) SKILL_SOURCE="$2"; shift 2 ;;
    --skill-root) SKILL_ROOT="$2"; shift 2 ;;
    *) shift ;;
  esac
done

log_debug() {
  if $VERBOSE; then
    echo "[DEBUG] $1"
  fi
}

get_workflow_version() {
  local path="$1"
  awk -F'|' '
    /^\|[[:space:]]*[0-9]+\.[0-9]+[[:space:]]*\|/ {
      gsub(/[[:space:]]/, "", $2);
      latest=$2;
    }
    END {
      if (latest != "") {
        print "v" latest;
      } else {
        print "unknown";
      }
    }
  ' "$path"
}

clone_or_update_repo() {
  local repo_url="$1"
  local target_path="$2"
  local label="$3"

  if [[ -d "$target_path/.git" ]]; then
    echo "Updating $label..."
    git -C "$target_path" pull --ff-only
    return
  fi

  if [[ -d "$target_path" ]] && [[ -n "$(ls -A "$target_path" 2>/dev/null)" ]]; then
    echo "Skip $label: target exists and is not an empty git repo ($target_path)."
    return
  fi

  echo "Cloning $label..."
  git clone --depth 1 "$repo_url" "$target_path"
}

install_skill() {
  local key="$1"
  local repo_url=""
  local target_suffix=""
  local label=""

  case "$key" in
    antigravity)
      repo_url="https://github.com/sickn33/antigravity-awesome-skills.git"
      target_suffix="skills"
      label="sickn33/antigravity-awesome-skills"
      ;;
    claude)
      repo_url="https://github.com/ComposioHQ/awesome-claude-skills.git"
      target_suffix="awesome-claude-skills"
      label="ComposioHQ/awesome-claude-skills"
      ;;
    anthropic)
      repo_url="https://github.com/anthropics/skills.git"
      target_suffix="anthropic-skills"
      label="anthropics/skills"
      ;;
    techleads)
      repo_url="https://github.com/tech-leads-club/agent-skills.git"
      target_suffix="techleads-agent-skills"
      label="tech-leads-club/agent-skills"
      ;;
    jeffallan)
      repo_url="https://github.com/Jeffallan/claude-skills.git"
      target_suffix="jeffallan-claude-skills"
      label="Jeffallan/claude-skills"
      ;;
    ui-ux-pro-max)
      repo_url="https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git"
      target_suffix="ui-ux-pro-max-skill"
      label="nextlevelbuilder/ui-ux-pro-max-skill"
      ;;
    othmanadi)
      repo_url="https://github.com/OthmanAdi/planning-with-files.git"
      target_suffix="othman-planning-with-files"
      label="OthmanAdi/planning-with-files"
      ;;
    scientific)
      repo_url="https://github.com/K-Dense-AI/claude-scientific-skills.git"
      target_suffix="claude-scientific-skills"
      label="K-Dense-AI/claude-scientific-skills"
      ;;
    all)
      for k in antigravity claude anthropic techleads jeffallan ui-ux-pro-max othmanadi scientific; do
        install_skill "$k"
      done
      return
      ;;
    *)
      echo "Unknown skill source: $key. Options: antigravity, claude, anthropic, techleads, jeffallan, ui-ux-pro-max, othmanadi, scientific, all"
      return 1
      ;;
  esac

  clone_or_update_repo "$repo_url" "$SKILL_ROOT/$target_suffix" "$label"
}

# ─── Prerequisite Check ─────────────────────────────────────────────────────
check_prerequisites() {
  # Check Git
  if ! command -v git &>/dev/null; then
    echo "❌ Git is required but not found."
    echo "   Install: https://git-scm.com/downloads"
    echo "   Or: brew install git / apt install git"
    exit 1
  fi
  log_debug "Git found: $(git --version)"

  # Check curl
  if ! command -v curl &>/dev/null; then
    echo "❌ curl is required but not found."
    exit 1
  fi
  log_debug "curl found: $(curl --version | head -1)"

  # Check internet
  if ! curl -sL --connect-timeout 5 "https://github.com" >/dev/null 2>&1; then
    echo "❌ Cannot reach GitHub. Check your internet connection."
    exit 1
  fi
  log_debug "Internet connectivity OK"
}

# ─── Uninstall ───────────────────────────────────────────────────────────────
if $UNINSTALL; then
  echo "AI Project Rules Generator - Uninstall"
  echo "======================================="
  echo

  for file in "$WORKFLOW_FILE" "${WORKFLOW_FILE}.backup"; do
    if [[ -f "$file" ]]; then
      rm -f "$file"
      echo "  Removed: $file"
    fi
  done

  # Remove empty directories
  if [[ -d ".agent/workflows" ]] && [[ -z "$(ls -A .agent/workflows 2>/dev/null)" ]]; then
    rmdir ".agent/workflows"
    echo "  Removed empty: .agent/workflows/"
  fi

  echo
  echo "Uninstall complete."
  echo "Note: Skill sources (.agent/skills/, shared skill roots, etc.) were NOT removed."
  echo "      Remove them manually if desired."
  echo "======================================="
  exit 0
fi

# ─── Update ──────────────────────────────────────────────────────────────────
if [[ "$ACTION" == "update" ]]; then
  echo "AI Project Rules Generator - Update"
  echo "==================================="
  echo

  check_prerequisites

  if [[ ! -f "$WORKFLOW_FILE" ]]; then
    echo "❌ Workflow not found at $WORKFLOW_FILE"
    echo "Run without --update to install first."
    exit 1
  fi

  cp "$WORKFLOW_FILE" "${WORKFLOW_FILE}.backup"
  echo "Backed up current workflow to ${WORKFLOW_FILE}.backup"

  echo "Downloading latest workflow..."
  curl -sL -o "$WORKFLOW_FILE" "${REPO_RAW}/workflows/create-project-rules.md"

  version="$(get_workflow_version "$WORKFLOW_FILE")"
  echo "✅ Workflow updated successfully."
  echo "Current version: $version"
  echo "Backup saved at: ${WORKFLOW_FILE}.backup"
  echo
  echo "Tip: Your .cursorrules and AGENTS.md are NOT affected."
  echo "Re-run /create-project-rules to regenerate with latest workflow."
  echo "==================================="
  exit 0
fi

# ─── Install ─────────────────────────────────────────────────────────────────
echo "AI Project Rules Generator - Quick Start Setup"
echo "==============================================="
echo

check_prerequisites

echo "Creating .agent/ directory structure..."
mkdir -p .agent/workflows "$SKILL_ROOT"

if [[ "$SKILL_ROOT" != ".agent" ]]; then
  echo "Using shared skill root: $SKILL_ROOT"
  echo "Keeping workflow local at $WORKFLOW_FILE"
fi

echo "Downloading workflow..."
curl -sL -o "$WORKFLOW_FILE" "${REPO_RAW}/workflows/create-project-rules.md"

version="$(get_workflow_version "$WORKFLOW_FILE")"
echo "✅ Workflow installed at $WORKFLOW_FILE (version: $version)"
echo

# ─── Skill Source Selection ──────────────────────────────────────────────────
if [[ -n "$SKILL_SOURCE" ]]; then
  install_skill "$SKILL_SOURCE" || true
elif $NON_INTERACTIVE; then
  echo "Non-interactive mode: skipping skill source selection."
  echo "Use --skill-source <name> to install skill sources."
  echo "Use --skill-root <path> to install sources into a shared skill root."
else
  echo "Recommended skill sources (optional):"
  echo "Install root for skill sources: $SKILL_ROOT"
  echo "  1) sickn33 / antigravity-awesome-skills  (CATALOG, large catalog index)"
  echo "  2) ComposioHQ / awesome-claude-skills    (FOLDER, community skill packs)"
  echo "  3) anthropics / skills                   (FOLDER, official Anthropic skills)"
  echo "  4) tech-leads-club / agent-skills        (FOLDER, curated registry)"
  echo "  5) Jeffallan / claude-skills             (FOLDER, broad full-stack set)"
  echo "  6) nextlevelbuilder / ui-ux-pro-max      (WORKFLOW, UI/UX design intel)"
  echo "  7) OthmanAdi / planning-with-files       (FOLDER, planning persistence)"
  echo "  8) K-Dense-AI / claude-scientific-skills (FOLDER, scientific/research workflows)"
  echo "  9) All of the above"
  echo " 10) Skip (add your own later)"
  echo
  read -r -p "Choose [1-10]: " choice < /dev/tty

  case "$choice" in
    1) install_skill "antigravity" ;;
    2) install_skill "claude" ;;
    3) install_skill "anthropic" ;;
    4) install_skill "techleads" ;;
    5) install_skill "jeffallan" ;;
    6) install_skill "ui-ux-pro-max" ;;
    7) install_skill "othmanadi" ;;
    8) install_skill "scientific" ;;
    9) install_skill "all" ;;
    10) echo "Skipping skill source installation." ;;
    *) echo "Invalid choice, skipping skill source installation." ;;
  esac
fi

echo
echo "==============================================="
echo "✅ Setup complete."
echo
echo "Next steps:"
echo "  1) Open your project in your AI assistant"
echo "  2) Run: /create-project-rules"
echo "  3) Get tailored .cursorrules + AGENTS.md"
echo
echo "Options:"
echo "  Update:      ./setup.sh --update"
echo "  Uninstall:   ./setup.sh --uninstall"
echo "  CI/CD mode:  ./setup.sh --non-interactive --skill-source all"
echo "  Shared root: ./setup.sh --skill-source all --skill-root /shared/.agent"
echo "  Verbose:     ./setup.sh --verbose"
echo
echo "Docs: https://github.com/naravid19/ai-project-rules-generator"
echo "==============================================="
