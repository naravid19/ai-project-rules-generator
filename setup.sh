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

if [[ "${1:-}" == "--update" || "${1:-}" == "-u" ]]; then
  echo "AI Project Rules Generator - Update"
  echo "==================================="
  echo

  if [[ ! -f "$WORKFLOW_FILE" ]]; then
    echo "Workflow not found at $WORKFLOW_FILE"
    echo "Run without --update to install first."
    exit 1
  fi

  cp "$WORKFLOW_FILE" "${WORKFLOW_FILE}.backup"
  echo "Backed up current workflow to ${WORKFLOW_FILE}.backup"

  echo "Downloading latest workflow..."
  curl -sL -o "$WORKFLOW_FILE" "${REPO_RAW}/workflows/create-project-rules.md"

  version="$(get_workflow_version "$WORKFLOW_FILE")"
  echo "Workflow updated successfully."
  echo "Current version: $version"
  echo "Backup saved at: ${WORKFLOW_FILE}.backup"
  echo
  echo "Tip: Your .cursorrules and AGENTS.md are NOT affected."
  echo "Re-run /create-project-rules to regenerate with latest workflow."
  echo "==================================="
  exit 0
fi

echo "AI Project Rules Generator - Quick Start Setup"
echo "==============================================="
echo

echo "Creating .agent/ directory structure..."
mkdir -p .agent/workflows .agent/skills

echo "Downloading workflow..."
curl -sL -o "$WORKFLOW_FILE" "${REPO_RAW}/workflows/create-project-rules.md"
echo "Workflow installed at $WORKFLOW_FILE"
echo

echo "Recommended skill sources (optional):"
echo "  1) antigravity-awesome-skills (CATALOG format)"
echo "  2) awesome-claude-skills (README format)"
echo "  3) All of the above"
echo "  4) Skip (add your own later)"
echo
read -r -p "Choose [1-4]: " choice

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

echo
echo "==============================================="
echo "Setup complete."
echo
echo "Next steps:"
echo "  1) Open your project in your AI assistant"
echo "  2) Run: /create-project-rules"
echo "  3) Get tailored .cursorrules + AGENTS.md"
echo
echo "Docs: https://github.com/naravid19/ai-project-rules-generator"
echo "Update later: ./setup.sh --update"
echo "==============================================="
