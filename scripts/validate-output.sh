#!/usr/bin/env bash
# =============================================================================
# Validate Output - AI Project Rules Generator
# =============================================================================
# Validates generated .cursorrules and AGENTS.md files with heuristic scoring.
# Usage: ./scripts/validate-output.sh [--path <project-root>] [--strict] [--threshold <n>]
# =============================================================================

set -euo pipefail

PROJECT_ROOT="."
STRICT_MODE=false
CLI_THRESHOLD=""
TOTAL_CHECKS=0
PASSED_CHECKS=0
WARNINGS=()
ERRORS=()

PLACEHOLDER_PATTERNS=(
  '\{[A-Z0-9_ -]+\}'
  '\{project'
  '___'
  '\bTBD\b'
  '\bTODO\b'
)

VAGUE_PATTERNS=(
  'write good code'
  'write clean code'
  'follow best practices'
  'be professional'
  '\betc\.\b'
)

REPO_LOCAL_PREFIXES=(
  "README.md"
  "AGENTS.md"
  ".cursorrules"
  "CHANGELOG.md"
  "setup.ps1"
  "setup.sh"
  "workflows/"
  "templates/"
  "scripts/"
  "i18n/"
  "images/"
  "log/"
)

declare -A REQUIRED_HEADINGS
REQUIRED_HEADINGS[".cursorrules"]="Project Identity|Project Structure|Coding Standards|Critical Rules|Code Smells"
REQUIRED_HEADINGS["AGENTS.md"]="Quick Context|Available Skills|Multi-Platform Output Mapping|Common Patterns|Non-Negotiable Constraints"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --path)
      PROJECT_ROOT="$2"
      shift 2
      ;;
    --strict)
      STRICT_MODE=true
      shift
      ;;
    --threshold)
      CLI_THRESHOLD="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

pass() {
  ((PASSED_CHECKS+=1))
  ((TOTAL_CHECKS+=1))
  echo "  [PASS] $1"
}

fail() {
  ((TOTAL_CHECKS+=1))
  ERRORS+=("$1")
  echo "  [FAIL] $1"
}

warn() {
  WARNINGS+=("$1")
  echo "  [WARN] $1"
}

strip_fenced_code_blocks() {
  python - "$1" <<'PY'
import re
import sys

print(re.sub(r"```.*?```", "", sys.stdin.read(), flags=re.S), end="")
PY
}

config_threshold() {
  local config_path="$PROJECT_ROOT/.rulesrc.yaml"
  if [[ ! -f "$config_path" ]]; then
    return 1
  fi

  local value
  value="$(sed -nE 's/^[[:space:]]*quality_threshold[[:space:]]*:[[:space:]]*([0-9]+)[[:space:]]*$/\1/p' "$config_path" | head -n 1)"
  if [[ -n "$value" ]]; then
    echo "$value"
    return 0
  fi

  return 1
}

effective_threshold() {
  local result

  if [[ -n "$CLI_THRESHOLD" ]]; then
    result="$CLI_THRESHOLD"
  elif result="$(config_threshold)"; then
    :
  else
    result="38"
  fi

  if $STRICT_MODE && [[ "$result" -lt 42 ]]; then
    result="42"
  fi

  echo "$result"
}

pattern_count() {
  local content="$1"
  shift
  python - "$content" "$@" <<'PY'
import re
import sys

content = sys.argv[1]
patterns = sys.argv[2:]
count = 0
for pattern in patterns:
    count += len(re.findall(pattern, content, flags=re.I))
print(count)
PY
}

heading_count() {
  local file="$1"
  grep -Ec '^#{1,6}[[:space:]]+' "$file" || true
}

table_count() {
  local file="$1"
  grep -Ec '^\|.+\|[[:space:]]*$' "$file" || true
}

code_block_count() {
  local file="$1"
  local ticks
  ticks="$(grep -Ec '^```' "$file" || true)"
  echo $((ticks / 2))
}

bullet_count() {
  local file="$1"
  grep -Ec '^[[:space:]]*([-*]|[0-9]+\.)[[:space:]]+' "$file" || true
}

long_paragraph_count() {
  python - "$1" <<'PY'
from pathlib import Path
import re
import sys

content = Path(sys.argv[1]).read_text(encoding="utf-8")
content = re.sub(r"```.*?```", "", content, flags=re.S)
blocks = re.split(r"(?:\r?\n){2,}", content)
count = 0
for block in blocks:
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    if len(lines) < 10:
        continue
    paragraph_lines = [line for line in lines if not re.match(r"^(#|>|[-*]|\d+\.|\|)", line)]
    if len(paragraph_lines) >= 10:
        count += 1
print(count)
PY
}

repo_local_path_errors() {
  python - "$1" "$PROJECT_ROOT" "${REPO_LOCAL_PREFIXES[@]}" <<'PY'
from pathlib import Path
import re
import sys

file_path = Path(sys.argv[1])
root = Path(sys.argv[2])
prefixes = tuple(sys.argv[3:])
content = file_path.read_text(encoding="utf-8")
candidates = set()

for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", content):
    candidates.add(match.group(1).strip())

for match in re.finditer(r"`([^`\r\n]+)`", content):
    candidates.add(match.group(1).strip())

errors = []
for candidate in candidates:
    if not candidate or re.match(r"^(https?:|mailto:|#)", candidate):
        continue
    normalized = candidate.replace("\\", "/").split("#", 1)[0]
    if not normalized or "*" in normalized or "{" in normalized or "}" in normalized:
        continue
    if not (normalized in prefixes or normalized.startswith(prefixes)):
        continue
    target = root / Path(normalized)
    if not target.exists():
        errors.append(normalized)

print("\n".join(sorted(set(errors))))
PY
}

hardcoded_skill_hits() {
  python - "$1" <<'PY'
from pathlib import Path
import re
import sys

content = Path(sys.argv[1]).read_text(encoding="utf-8")
content = re.sub(r"```.*?```", "", content, flags=re.S)
markers = ("Hardcoding", "BAD", "Anti-Pattern", "Instead Do")
hits = set()
for line in content.splitlines():
    if any(marker in line for marker in markers):
        continue
    hits.update(re.findall(r"@[a-z0-9][a-z0-9-]*", line, flags=re.I))
print("\n".join(sorted(hits)))
PY
}

meaningful_line_count() {
  python - "$1" "$2" <<'PY'
from pathlib import Path
import re
import sys

primary = Path(sys.argv[1]).read_text(encoding="utf-8")
secondary = Path(sys.argv[2]).read_text(encoding="utf-8")

def normalize(text: str):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    items = set()
    for raw in text.splitlines():
        line = raw.strip()
        if len(line) < 30:
            continue
        if re.match(r"^\|[- :]+\|?$", line):
            continue
        if re.match(r"^(```|#|>|[-*]|\d+\.)", line):
            continue
        items.add(line)
    return items

print(len(normalize(primary) & normalize(secondary)))
PY
}

score_file() {
  local file_name="$1"
  local full_path="$PROJECT_ROOT/$file_name"
  local headings_raw="${REQUIRED_HEADINGS[$file_name]}"

  local exists=0
  local line_count=0
  local heading_total=0
  local table_total=0
  local code_total=0
  local bullet_total=0
  local long_paragraphs=0
  local required_found=0
  local placeholder_hits=0
  local vague_hits=0
  local hardcoded_hits=0
  local repo_errors=0

  if [[ ! -f "$full_path" ]]; then
    fail "Missing $file_name"
    echo "0|0|0|0|0|0|0|0|0|0|0|0"
    return
  fi

  exists=1
  line_count="$(wc -l < "$full_path" | tr -d ' ')"
  heading_total="$(heading_count "$full_path")"
  table_total="$(table_count "$full_path")"
  code_total="$(code_block_count "$full_path")"
  bullet_total="$(bullet_count "$full_path")"
  long_paragraphs="$(long_paragraph_count "$full_path")"

  pass "Found $file_name"
  pass "$file_name line count: $line_count"

  IFS='|' read -r -a headings <<< "$headings_raw"
  for heading in "${headings[@]}"; do
    if grep -Fqi "$heading" "$full_path"; then
      ((required_found+=1))
      pass "$file_name contains '$heading'"
    else
      fail "$file_name missing '$heading'"
    fi
  done

  local raw_content sanitized_content
  raw_content="$(cat "$full_path")"
  sanitized_content="$(strip_fenced_code_blocks <<< "$raw_content")"

  placeholder_hits="$(pattern_count "$raw_content" "${PLACEHOLDER_PATTERNS[@]}")"
  if [[ "$placeholder_hits" -eq 0 ]]; then
    pass "$file_name has no unresolved placeholders"
  else
    warn "$file_name contains placeholder-like content: $placeholder_hits"
  fi

  local repo_error_list
  repo_error_list="$(repo_local_path_errors "$full_path")"
  if [[ -z "$repo_error_list" ]]; then
    pass "$file_name has no broken repo-local path references"
  else
    repo_errors="$(printf '%s\n' "$repo_error_list" | sed '/^$/d' | wc -l | tr -d ' ')"
    warn "$file_name contains broken repo-local path references: $(printf '%s' "$repo_error_list" | tr '\n' ',' | sed 's/,$//')"
  fi

  vague_hits="$(pattern_count "$sanitized_content" "${VAGUE_PATTERNS[@]}")"
  if [[ "$vague_hits" -eq 0 ]]; then
    pass "$file_name avoids vague rule phrasing"
  else
    warn "$file_name contains vague phrasing: $vague_hits"
  fi

  local hardcoded_list
  hardcoded_list="$(hardcoded_skill_hits "$full_path")"
  if [[ -z "$hardcoded_list" ]]; then
    pass "$file_name has no positive-context hardcoded skill invocations"
  else
    hardcoded_hits="$(printf '%s\n' "$hardcoded_list" | sed '/^$/d' | wc -l | tr -d ' ')"
    warn "$file_name contains literal skill invocations: $(printf '%s' "$hardcoded_list" | tr '\n' ',' | sed 's/,$//')"
  fi

  if [[ "$table_total" -gt 0 ]]; then
    pass "$file_name includes tabular structure"
  else
    warn "$file_name has no markdown tables"
  fi

  if [[ "$code_total" -gt 0 ]]; then
    pass "$file_name includes fenced code blocks"
  else
    warn "$file_name has no fenced code blocks"
  fi

  if [[ "$long_paragraphs" -eq 0 ]]; then
    pass "$file_name avoids long wall-of-text paragraphs"
  else
    warn "$file_name has long paragraph blocks: $long_paragraphs"
  fi

  local completeness accuracy specificity scannability

  completeness=$((required_found * 2))

  accuracy=10
  accuracy=$((accuracy - (placeholder_hits * 2)))
  if [[ "$accuracy" -lt 4 ]]; then
    accuracy=$((10 - 6))
  fi
  accuracy=$((accuracy - repo_errors))
  if [[ "$accuracy" -lt 0 ]]; then accuracy=0; fi

  specificity=10
  if [[ "$table_total" -eq 0 ]]; then specificity=$((specificity - 2)); fi
  if [[ "$code_total" -eq 0 ]]; then specificity=$((specificity - 2)); fi
  if ! grep -Eqi '\bexample\b|for example|\bgood\b|\bbad\b' "$full_path"; then
    specificity=$((specificity - 2))
  fi
  local vague_penalty=$((vague_hits * 2))
  if [[ "$vague_penalty" -gt 4 ]]; then vague_penalty=4; fi
  specificity=$((specificity - vague_penalty))
  if [[ "$specificity" -lt 0 ]]; then specificity=0; fi

  scannability=10
  if [[ "$heading_total" -lt 5 ]]; then scannability=$((scannability - 2)); fi
  if [[ "$bullet_total" -lt 5 ]]; then scannability=$((scannability - 2)); fi
  if [[ "$table_total" -eq 0 ]]; then scannability=$((scannability - 1)); fi
  local paragraph_penalty=$((long_paragraphs * 2))
  if [[ "$paragraph_penalty" -gt 5 ]]; then paragraph_penalty=5; fi
  scannability=$((scannability - paragraph_penalty))
  if [[ "$scannability" -lt 0 ]]; then scannability=0; fi

  echo "$exists|$line_count|$completeness|$accuracy|$specificity|$scannability|$hardcoded_hits|$placeholder_hits|$repo_errors|$table_total|$code_total|$long_paragraphs"
}

PROJECT_ROOT="$(cd "$PROJECT_ROOT" && pwd)"
THRESHOLD="$(effective_threshold)"

echo
echo "============================================================"
echo " AI Project Rules Generator - Output Validation"
echo "============================================================"
echo
echo "  Project:   $PROJECT_ROOT"
echo "  Threshold: $THRESHOLD/50"
echo "  Strict:    $( $STRICT_MODE && echo on || echo off )"

IFS='|' read -r CURSOR_EXISTS CURSOR_LINES CURSOR_COMPLETENESS CURSOR_ACCURACY CURSOR_SPECIFICITY CURSOR_SCANNABILITY CURSOR_HARDCODED CURSOR_PLACEHOLDERS CURSOR_REPO_ERRORS CURSOR_TABLES CURSOR_CODE CURSOR_PARAGRAPHS <<< "$(score_file ".cursorrules")"
IFS='|' read -r AGENTS_EXISTS AGENTS_LINES AGENTS_COMPLETENESS AGENTS_ACCURACY AGENTS_SPECIFICITY AGENTS_SCANNABILITY AGENTS_HARDCODED AGENTS_PLACEHOLDERS AGENTS_REPO_ERRORS AGENTS_TABLES AGENTS_CODE AGENTS_PARAGRAPHS <<< "$(score_file "AGENTS.md")"

CURSOR_DUPLICATION=0
AGENTS_DUPLICATION=0
if [[ "$CURSOR_EXISTS" -eq 1 && "$AGENTS_EXISTS" -eq 1 ]]; then
  CURSOR_DUPLICATION="$(meaningful_line_count "$PROJECT_ROOT/.cursorrules" "$PROJECT_ROOT/AGENTS.md")"
  AGENTS_DUPLICATION="$CURSOR_DUPLICATION"
fi

CURSOR_CONSISTENCY=10
if [[ "$CURSOR_HARDCODED" -gt 0 ]]; then
  CURSOR_CONSISTENCY=$((CURSOR_CONSISTENCY - 6))
fi
if [[ "$CURSOR_DUPLICATION" -gt 12 ]]; then
  CURSOR_CONSISTENCY=$((CURSOR_CONSISTENCY - 4))
elif [[ "$CURSOR_DUPLICATION" -gt 6 ]]; then
  CURSOR_CONSISTENCY=$((CURSOR_CONSISTENCY - 2))
fi
if [[ "$CURSOR_CONSISTENCY" -lt 0 ]]; then CURSOR_CONSISTENCY=0; fi

AGENTS_CONSISTENCY=10
if [[ "$AGENTS_HARDCODED" -gt 0 ]]; then
  AGENTS_CONSISTENCY=$((AGENTS_CONSISTENCY - 6))
fi
if [[ "$AGENTS_DUPLICATION" -gt 12 ]]; then
  AGENTS_CONSISTENCY=$((AGENTS_CONSISTENCY - 4))
elif [[ "$AGENTS_DUPLICATION" -gt 6 ]]; then
  AGENTS_CONSISTENCY=$((AGENTS_CONSISTENCY - 2))
fi
if [[ "$AGENTS_CONSISTENCY" -lt 0 ]]; then AGENTS_CONSISTENCY=0; fi

CURSOR_TOTAL=$((CURSOR_COMPLETENESS + CURSOR_ACCURACY + CURSOR_SPECIFICITY + CURSOR_SCANNABILITY + CURSOR_CONSISTENCY))
AGENTS_TOTAL=$((AGENTS_COMPLETENESS + AGENTS_ACCURACY + AGENTS_SPECIFICITY + AGENTS_SCANNABILITY + AGENTS_CONSISTENCY))

write_scorecard() {
  local file_name="$1"
  local completeness="$2"
  local accuracy="$3"
  local specificity="$4"
  local scannability="$5"
  local consistency="$6"
  local total="$7"
  local duplication="$8"

  echo
  echo "$file_name Scorecard:"
  echo "  Completeness: $completeness/10"
  echo "  Accuracy:     $accuracy/10"
  echo "  Specificity:  $specificity/10"
  echo "  Scannability: $scannability/10"
  echo "  Consistency:  $consistency/10"
  echo "  Total:        $total/50"

  if [[ "$duplication" -gt 12 ]]; then
    warn "$file_name duplicates too much content across files ($duplication common lines)"
  elif [[ "$duplication" -gt 6 ]]; then
    warn "$file_name has moderate cross-file duplication ($duplication common lines)"
  else
    pass "$file_name keeps cross-file duplication low ($duplication common lines)"
  fi

  if [[ "$total" -ge "$THRESHOLD" ]]; then
    pass "$file_name meets threshold $THRESHOLD/50"
  else
    fail "$file_name fails threshold $THRESHOLD/50"
  fi
}

write_scorecard ".cursorrules" "$CURSOR_COMPLETENESS" "$CURSOR_ACCURACY" "$CURSOR_SPECIFICITY" "$CURSOR_SCANNABILITY" "$CURSOR_CONSISTENCY" "$CURSOR_TOTAL" "$CURSOR_DUPLICATION"
write_scorecard "AGENTS.md" "$AGENTS_COMPLETENESS" "$AGENTS_ACCURACY" "$AGENTS_SPECIFICITY" "$AGENTS_SCANNABILITY" "$AGENTS_CONSISTENCY" "$AGENTS_TOTAL" "$AGENTS_DUPLICATION"

echo
echo "============================================================"
echo " Validation Summary"
echo "============================================================"
echo "  Raw checks passed: $PASSED_CHECKS/$TOTAL_CHECKS"
echo "  Warnings:          ${#WARNINGS[@]}"
echo "  Errors:            ${#ERRORS[@]}"
echo "  .cursorrules:      $CURSOR_TOTAL/50"
echo "  AGENTS.md:         $AGENTS_TOTAL/50"
echo

if [[ "${#ERRORS[@]}" -eq 0 ]]; then
  echo "  Result: PASS"
else
  echo "  Result: FAIL"
  for error_message in "${ERRORS[@]}"; do
    echo "    - $error_message"
  done
fi

if [[ "${#WARNINGS[@]}" -gt 0 ]]; then
  echo
  echo "  Warning Details:"
  for warning_message in "${WARNINGS[@]}"; do
    echo "    - $warning_message"
  done
fi

echo
echo "============================================================"

if [[ "${#ERRORS[@]}" -gt 0 ]]; then
  exit 1
fi
