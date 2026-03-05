#!/usr/bin/env bash
# =============================================================================
# Validate Output — AI Project Rules Generator
# =============================================================================
# Validates generated .cursorrules and AGENTS.md files for quality.
# Usage: ./scripts/validate-output.sh [--path <project-root>] [--strict]
# =============================================================================

set -euo pipefail

# ─── Configuration ───────────────────────────────────────────────────────────
PROJECT_ROOT="."
STRICT_MODE=false
PASS_THRESHOLD=38
TOTAL_SCORE=0
TOTAL_CHECKS=0
PASSED_CHECKS=0
WARNINGS=()
ERRORS=()

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --path) PROJECT_ROOT="$2"; shift 2 ;;
    --strict) STRICT_MODE=true; shift ;;
    --threshold) PASS_THRESHOLD="$2"; shift 2 ;;
    *) shift ;;
  esac
done

# ─── Helper Functions ────────────────────────────────────────────────────────
pass() { ((PASSED_CHECKS++)); ((TOTAL_CHECKS++)); echo "  ✅ $1"; }
fail() { ((TOTAL_CHECKS++)); ERRORS+=("$1"); echo "  ❌ $1"; }
warn() { WARNINGS+=("$1"); echo "  ⚠️  $1"; }

check_file_exists() {
  if [[ -f "$PROJECT_ROOT/$1" ]]; then
    pass "Found $1"
    return 0
  else
    fail "Missing $1"
    return 1
  fi
}

check_section_exists() {
  local file="$1"
  local section="$2"
  if grep -qi "$section" "$PROJECT_ROOT/$file" 2>/dev/null; then
    pass "$file contains '$section'"
    return 0
  else
    fail "$file missing section '$section'"
    return 1
  fi
}

check_no_hardcoded_skills() {
  local file="$1"
  if grep -qE '@[a-z]+-[a-z]+' "$PROJECT_ROOT/$file" 2>/dev/null; then
    fail "$file contains hardcoded skill names (@skill-name pattern)"
    return 1
  else
    pass "$file has no hardcoded skill names"
    return 0
  fi
}

count_lines() {
  wc -l < "$PROJECT_ROOT/$1" 2>/dev/null | tr -d ' '
}

# ─── Main Validation ─────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   AI Project Rules Generator — Output Validation        ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "  Project: $PROJECT_ROOT"
echo "  Threshold: $PASS_THRESHOLD/50"
echo ""

# ─── Check 1: File Existence ─────────────────────────────────────────────────
echo "📁 File Existence:"
HAS_CURSORRULES=false
HAS_AGENTS=false

if check_file_exists ".cursorrules"; then HAS_CURSORRULES=true; fi
if check_file_exists "AGENTS.md"; then HAS_AGENTS=true; fi
echo ""

# ─── Check 2: .cursorrules Structure ─────────────────────────────────────────
if $HAS_CURSORRULES; then
  echo "📋 .cursorrules Structure:"
  check_section_exists ".cursorrules" "Project Identity"
  check_section_exists ".cursorrules" "Coding Standards"
  check_section_exists ".cursorrules" "Critical Rules"
  check_section_exists ".cursorrules" "Code Smells"

  LINES=$(count_lines ".cursorrules")
  if [[ "$LINES" -ge 100 ]]; then
    pass ".cursorrules has sufficient content ($LINES lines)"
  elif [[ "$LINES" -ge 50 ]]; then
    warn ".cursorrules is short ($LINES lines, recommended: 150-400)"
  else
    fail ".cursorrules is too short ($LINES lines, minimum: 100)"
  fi

  check_no_hardcoded_skills ".cursorrules"
  echo ""
fi

# ─── Check 3: AGENTS.md Structure ────────────────────────────────────────────
if $HAS_AGENTS; then
  echo "📋 AGENTS.md Structure:"
  check_section_exists "AGENTS.md" "Quick Context"
  check_section_exists "AGENTS.md" "Available Skills"
  check_section_exists "AGENTS.md" "Constraints"

  LINES=$(count_lines "AGENTS.md")
  if [[ "$LINES" -ge 80 ]]; then
    pass "AGENTS.md has sufficient content ($LINES lines)"
  elif [[ "$LINES" -ge 40 ]]; then
    warn "AGENTS.md is short ($LINES lines, recommended: 100-250)"
  else
    fail "AGENTS.md is too short ($LINES lines, minimum: 80)"
  fi

  check_no_hardcoded_skills "AGENTS.md"
  echo ""
fi

# ─── Check 4: Content Smells ─────────────────────────────────────────────────
echo "🔍 Content Smell Detection:"

for file in ".cursorrules" "AGENTS.md"; do
  if [[ -f "$PROJECT_ROOT/$file" ]]; then
    # Check for vague rules
    if grep -qi "write good code\|write clean code\|follow best practices" "$PROJECT_ROOT/$file" 2>/dev/null; then
      warn "$file contains vague rules (e.g., 'write good code')"
    else
      pass "$file has no vague rules"
    fi

    # Check for walls of text (sections > 15 lines without headers)
    if awk '/^##/{c=0} {c++} c>15{found=1; exit} END{exit !found}' "$PROJECT_ROOT/$file" 2>/dev/null; then
      warn "$file may contain walls of text (sections >15 lines without sub-headers)"
    fi
  fi
done
echo ""

# ─── Check 5: Consistency ────────────────────────────────────────────────────
if $HAS_CURSORRULES && $HAS_AGENTS; then
  echo "🔗 Cross-File Consistency:"

  # Check for duplicate content
  COMMON_LINES=$(comm -12 \
    <(grep -v "^$\|^#\|^-\|^|\|^\`" "$PROJECT_ROOT/.cursorrules" 2>/dev/null | sort -u) \
    <(grep -v "^$\|^#\|^-\|^|\|^\`" "$PROJECT_ROOT/AGENTS.md" 2>/dev/null | sort -u) | wc -l)

  if [[ "$COMMON_LINES" -lt 5 ]]; then
    pass "Minimal content duplication between files ($COMMON_LINES common lines)"
  else
    warn "Possible content duplication ($COMMON_LINES common lines)"
  fi
  echo ""
fi

# ─── Summary ─────────────────────────────────────────────────────────────────
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📊 Validation Summary:"
echo "   Checks: $PASSED_CHECKS/$TOTAL_CHECKS passed"
echo "   Warnings: ${#WARNINGS[@]}"
echo "   Errors: ${#ERRORS[@]}"
echo ""

if [[ ${#ERRORS[@]} -eq 0 ]]; then
  echo "  ✅ PASSED — All checks passed!"
else
  echo "  ❌ FAILED — ${#ERRORS[@]} error(s) found:"
  for err in "${ERRORS[@]}"; do
    echo "     • $err"
  done
fi

if [[ ${#WARNINGS[@]} -gt 0 ]]; then
  echo ""
  echo "  ⚠️  Warnings:"
  for warn_msg in "${WARNINGS[@]}"; do
    echo "     • $warn_msg"
  done
fi

echo ""
echo "═══════════════════════════════════════════════════════════"

# Exit with error if there are failures
if [[ ${#ERRORS[@]} -gt 0 ]]; then
  exit 1
fi
