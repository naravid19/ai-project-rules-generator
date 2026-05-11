# 🌐 Multi-Language Support

Guidelines for generating `.cursorrules` and `AGENTS.md` in multiple languages.

## Supported Languages

| Code | Language               | Status       |
| ---- | ---------------------- | ------------ |
| `en` | English                | ✅ Default   |
| `th` | ไทย (Thai)             | ✅ Supported |
| `ja` | 日本語 (Japanese)      | ✅ Supported |
| `zh` | 中文 (Chinese)         | ✅ Supported |
| `ko` | 한국어 (Korean)        | ✅ Supported |
| `es` | Español (Spanish)      | ✅ Supported |
| `fr` | Français (French)      | ✅ Supported |
| `de` | Deutsch (German)       | ✅ Supported |
| `pt` | Português (Portuguese) | ✅ Supported |

## How Language Selection Works

### Automatic Detection

The workflow detects project language from:

1. **Config file** — `.rulesrc.yaml` → `output_language` field
2. **README.md language** — if the project's README is in Thai, default to Thai
3. **Interactive prompt** — Stage 0 asks the user (if interactive mode is on)
4. **Fallback** — defaults to English (`en`)

### What Gets Translated

| Element           | Translated? | Notes                                           |
| ----------------- | ----------- | ----------------------------------------------- |
| Section headers   | ✅ Yes      | `## Critical Rules` → `## กฎสำคัญ (Critical)`   |
| Rule descriptions | ✅ Yes      | Natural language descriptions                   |
| Code examples     | ❌ No       | Code stays in the original programming language |
| Variable names    | ❌ No       | Follow project's naming conventions             |
| Emoji/icons       | ❌ No       | Universal across all languages                  |
| Technical terms   | ⚠️ Partial  | Keep original term in parentheses               |

### Translation Pattern

When translating, always keep the original English technical term in parentheses for clarity:

```markdown
## กฎสำคัญ (Critical Rules) 🔴

### กฎที่ 1: ❌ ห้าม hardcode ชื่อ skill

**ทำไม**: Skill มีการเพิ่ม/เปลี่ยนชื่อ/อัปเดตอยู่ตลอด การ hardcode จะทำให้ไฟล์ล้าสมัยทันที
```

## How to Add a New Language

1. Add the language code to the supported languages table above
2. The AI will automatically generate content in the requested language
3. No additional template files are needed — the workflow handles translation dynamically

> [!TIP]
> You don't need to create separate template files for each language. The workflow generates translated content dynamically based on the language setting.

## Configuration

Set the output language in `.rulesrc.yaml`:

```yaml
output_language: th
```

Or specify during the interactive prompt (Stage 0):

```
> Preferred output language? [en/th/ja/zh/ko/es/fr/de/pt]: th
```
