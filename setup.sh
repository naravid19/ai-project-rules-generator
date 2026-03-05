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
  echo "Note: Skill sources (.agent/skills/, .agent/awesome-claude-skills/) were NOT removed."
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
mkdir -p .agent/workflows .agent/skills

echo "Downloading workflow..."
curl -sL -o "$WORKFLOW_FILE" "${REPO_RAW}/workflows/create-project-rules.md"

version="$(get_workflow_version "$WORKFLOW_FILE")"
echo "✅ Workflow installed at $WORKFLOW_FILE (version: $version)"
echo

# ─── Skill Source Selection ──────────────────────────────────────────────────
if [[ -n "$SKILL_SOURCE" ]]; then
  case "$SKILL_SOURCE" in
    antigravity)
      clone_or_update_repo "https://github.com/sickn33/antigravity-awesome-skills.git" ".agent/skills" "antigravity-awesome-skills"
      ;;
    claude)
      clone_or_update_repo "https://github.com/ComposioHQ/awesome-claude-skills.git" ".agent/awesome-claude-skills" "awesome-claude-skills"
      ;;
    all)
      clone_or_update_repo "https://github.com/sickn33/antigravity-awesome-skills.git" ".agent/skills" "antigravity-awesome-skills"
      clone_or_update_repo "https://github.com/ComposioHQ/awesome-claude-skills.git" ".agent/awesome-claude-skills" "awesome-claude-skills"
      ;;
    *)
      echo "Unknown skill source: $SKILL_SOURCE. Options: antigravity, claude, all"
      ;;
  esac
elif $NON_INTERACTIVE; then
  echo "Non-interactive mode: skipping skill source selection."
  echo "Use --skill-source <name> to install skill sources."
else
  echo "Recommended skill sources (optional):"
  echo "  1) antigravity-awesome-skills (CATALOG format, 968+ skills)"
  echo "  2) awesome-claude-skills (README format, 30+ skills)"
  echo "  3) All of the above"
  echo "  4) Skip (add your own later)"
  echo
  read -r -p "Choose [1-4]: " choice < /dev/tty

  case "$choice" in
    1)
      clone_or_update_repo "https://github.com/sickn33/antigravity-awesome-skills.git" ".agent/skills" "antigravity-awesome-skills"
      ;;
    2)
      clone_or_update_repo "https://github.com/ComposioHQ/awesome-claude-skills.git" ".agent/awesome-claude-skills" "awesome-claude-skills"
      ;;
    3)
      clone_or_update_repo "https://github.com/sickn33/antigravity-awesome-skills.git" ".agent/skills" "antigravity-awesome-skills"
      clone_or_update_repo "https://github.com/ComposioHQ/awesome-claude-skills.git" ".agent/awesome-claude-skills" "awesome-claude-skills"
      ;;
    4)
      echo "Skipping skill source installation."
      ;;
    *)
      echo "Invalid choice, skipping skill source installation."
      ;;
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
echo "  Verbose:     ./setup.sh --verbose"
echo
echo "Docs: https://github.com/naravid19/ai-project-rules-generator"
echo "==============================================="
