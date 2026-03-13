from __future__ import annotations

import sys
from pathlib import Path


class ConfigWizard:
    """Interactive CLI wizard to generate `.rulesrc.yaml`."""

    PLATFORMS = [
        "cursor",
        "claude",
        "antigravity",
        "gemini",
        "codex",
        "kiro",
        "copilot",
        "opencode",
        "adal",
    ]
    SEVERITIES = ["strict", "balanced", "relaxed"]
    LANGUAGES = ["en", "th", "ja", "zh", "ko", "es", "fr", "de", "pt"]
    STYLES = ["progressive", "flat", "minimal"]
    OPTIONAL_SECTIONS = [
        "security",
        "accessibility",
        "i18n",
        "performance",
        "git-workflow",
        "api-design",
    ]

    def __init__(self) -> None:
        self.config: dict[str, object] = {}

    def run(self) -> None:
        """Run the interactive prompt sequence."""
        self._print_header()

        try:
            self.config["target_platforms"] = self._ask_multi_choice(
                "Which AI tools do you use?",
                self.PLATFORMS,
                ["cursor", "codex"],
            )
            self.config["severity_level"] = self._ask_choice(
                "Select severity level for rules:",
                self.SEVERITIES,
                1,
            )
            self.config["output_language"] = self._ask_choice(
                "Select output language:",
                self.LANGUAGES,
                0,
            )
            self.config["include_sections"] = self._ask_multi_choice(
                "Select optional sections to include:",
                self.OPTIONAL_SECTIONS,
                [],
            )
            self.config["template_style"] = self._ask_choice(
                "Select template style:",
                self.STYLES,
                0,
            )
            self.config["preview_mode"] = self._ask_yes_no(
                "Show preview before writing files?",
                False,
            )
            self.config["quality_threshold"] = self._ask_threshold(38)

            self._generate_yaml()
            print("\nSuccess: .rulesrc.yaml has been created in your project root.")
        except KeyboardInterrupt:
            print("\n\nWizard cancelled.")
            sys.exit(0)

    def _print_header(self) -> None:
        print("==========================================================")
        print("AI Project Rules Generator - Interactive Wizard")
        print("==========================================================")
        print("This wizard will help you create a .rulesrc.yaml file")
        print("to customize your rule generation process.")
        print("==========================================================\n")

    def _ask_choice(self, question: str, options: list[str], default_index: int) -> str:
        print(f"\n{question}")
        for index, option in enumerate(options, start=1):
            print(f"  {index}. {option}")

        default_value = options[default_index]
        raw_choice = input(
            f"\nSelect an option [1-{len(options)}] (default: {default_value}): "
        ).strip()

        if not raw_choice:
            return default_value

        try:
            selected_index = int(raw_choice) - 1
        except ValueError:
            return default_value

        if 0 <= selected_index < len(options):
            return options[selected_index]
        return default_value

    def _ask_multi_choice(
        self,
        question: str,
        options: list[str],
        default: list[str],
    ) -> list[str]:
        print(f"\n{question} (comma-separated numbers)")
        for index, option in enumerate(options, start=1):
            print(f"  {index}. {option}")

        default_label = ", ".join(default) if default else "none"
        raw_choice = input(
            f"\nSelect options [e.g., 1,2,4] (default: {default_label}): "
        ).strip()
        if not raw_choice:
            return list(default)

        selected: list[str] = []
        try:
            indices = [int(chunk.strip()) - 1 for chunk in raw_choice.split(",")]
        except ValueError:
            return list(default)

        for index in indices:
            if 0 <= index < len(options):
                option = options[index]
                if option not in selected:
                    selected.append(option)

        return selected or list(default)

    def _ask_yes_no(self, question: str, default: bool) -> bool:
        default_label = "yes" if default else "no"
        raw_choice = input(f"\n{question} (yes/no) [default: {default_label}]: ").strip().lower()
        if not raw_choice:
            return default
        return raw_choice.startswith("y")

    def _ask_threshold(self, default: int) -> int:
        raw_choice = input(f"\nSet quality threshold (0-50) [default: {default}]: ").strip()
        if not raw_choice:
            return default

        try:
            value = int(raw_choice)
        except ValueError:
            return default

        if 0 <= value <= 50:
            return value
        return default

    def _generate_yaml(self) -> None:
        platforms = self.config["target_platforms"]
        include_sections = self.config.get("include_sections", [])

        platforms_yaml = "\n".join(f"  - {platform}" for platform in platforms)
        sections_yaml = "\n".join(f"    - {section}" for section in include_sections)
        optional_section_block = f"{sections_yaml}\n" if sections_yaml else ""

        yaml_content = f"""# .rulesrc.yaml generated by Interactive Wizard
target_platforms:
{platforms_yaml}

severity_level: {self.config['severity_level']}
output_language: {self.config['output_language']}

sections:
  include:
    - project-identity
    - coding-standards
    - critical-rules
    - important-guidelines
    - code-smells
    - testing
{optional_section_block}  exclude: []

template_style: {self.config['template_style']}
quality_threshold: {self.config['quality_threshold']}
preview_mode: {'true' if self.config['preview_mode'] else 'false'}
existing_files: ask
"""
        Path(".rulesrc.yaml").write_text(yaml_content, encoding="utf-8")


def main() -> None:
    wizard = ConfigWizard()
    wizard.run()


if __name__ == "__main__":
    main()
