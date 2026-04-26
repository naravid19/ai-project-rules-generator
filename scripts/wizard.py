from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from audit import audit_logger
from project_rules_runtime import score_project_confidence
from rules_config import SkillSourceConfig, format_yaml_path, load_confirmed_skill_sources


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
    DEFAULT_CONFIDENCE_THRESHOLD = 80
    DEFAULT_SKILL_MATCH_LIMIT = 5
    DEFAULT_AGENTIC_MATCH_LIMIT = 3

    def __init__(self) -> None:
        self.config: dict[str, object] = {}

    @audit_logger(action="wizard-config", platform="cli")
    def run(self) -> dict[str, Any]:
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
            selected_source, fallback_sources = self._ask_confirmed_skill_source()
            self.config["confirmed_skill_source"] = selected_source
            self.config["fallback_skill_sources"] = fallback_sources
            self.config["quality_threshold"] = self._ask_threshold(38)
            self.config["confidence_threshold"] = self._ask_threshold(
                self.DEFAULT_CONFIDENCE_THRESHOLD,
                prompt="Set confidence threshold (0-100) for human-in-the-loop clarification",
                maximum=100,
            )
            self.config["skill_match_limit"] = self._ask_threshold(
                self.DEFAULT_SKILL_MATCH_LIMIT,
                prompt="Set skill match limit to avoid context overload",
                maximum=100,
            )
            self._handle_confidence_gate(
                Path("."),
                int(self.config["confidence_threshold"]),
            )

            self._generate_yaml()
            print("\nSuccess: .rulesrc.yaml has been created in your project root.")
            return {"output_files": [".rulesrc.yaml"], "verification_status": "success"}
        except KeyboardInterrupt:
            print("\n\nWizard cancelled.")
            sys.exit(0)

    def _print_header(self) -> None:
        print("==========================================================")
        print("AI Project Rules Generator - Interactive Wizard")
        print("==========================================================")
        print("This wizard will help you create a .rulesrc.yaml file")
        print("to customize your rule generation process.")
        print("It will also force one confirmed skill source root.")
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

    def _ask_confirmed_skill_source(self) -> tuple[SkillSourceConfig, list[SkillSourceConfig]]:
        existing_confirmed = load_confirmed_skill_sources(Path(".rulesrc.yaml"))
        unique_existing = self._dedupe_sources(existing_confirmed)

        print("\nSelect the confirmed skill source root for this session:")
        options: list[SkillSourceConfig] = [SkillSourceConfig(path=".agent", confirmed=True)]

        if unique_existing:
            print("\nPreviously confirmed skill sources:")
            for index, source in enumerate(unique_existing, start=1):
                print(f"  {index}. {source.path}")
            options.extend(source for source in unique_existing if source.path != ".agent")

        print("\nAvailable choices:")
        for index, option in enumerate(options, start=1):
            label = "project-local default" if option.path == ".agent" else "re-use confirmed"
            print(f"  {index}. {option.path} ({label})")
        custom_choice_index = len(options) + 1
        print(f"  {custom_choice_index}. Enter a new skill source path")

        raw_choice = input(
            f"\nSelect confirmed skill source [1-{custom_choice_index}] (default: 1): "
        ).strip()

        if not raw_choice:
            selected = options[0]
        else:
            try:
                selected_index = int(raw_choice)
            except ValueError:
                selected_index = 1

            if selected_index == custom_choice_index:
                new_path = input("\nEnter skill source root path: ").strip() or ".agent"
                selected = SkillSourceConfig(path=new_path, confirmed=True)
            elif 1 <= selected_index <= len(options):
                selected = options[selected_index - 1]
            else:
                selected = options[0]

        fallback_sources: list[SkillSourceConfig] = []
        if selected.path != ".agent":
            fallback_sources.append(SkillSourceConfig(path=".agent", confirmed=False))

        return SkillSourceConfig(
            path=selected.path,
            format=selected.format,
            confirmed=True,
        ), fallback_sources

    def _ask_threshold(self, default: int, prompt: str = "Set quality threshold (0-50)", maximum: int = 50) -> int:
        raw_choice = input(f"\n{prompt} [default: {default}]: ").strip()
        if not raw_choice:
            return default

        try:
            value = int(raw_choice)
        except ValueError:
            return default

        if 0 <= value <= maximum:
            return value
        return default

    def _dedupe_sources(self, sources: list[SkillSourceConfig]) -> list[SkillSourceConfig]:
        unique: list[SkillSourceConfig] = []
        for source in sources:
            if any(existing.path == source.path for existing in unique):
                continue
            unique.append(source)
        return unique

    def _handle_confidence_gate(self, project_root: Path, threshold: int) -> None:
        result = score_project_confidence(project_root, threshold=threshold)
        self.config["detected_confidence_score"] = result.score

        if not result.requires_clarification:
            return

        print("\nConfidence gate triggered.")
        print(f"Detected confidence score: {result.score}/{threshold}")
        print("Choose the project intent before generation continues:")
        for index, option in enumerate(result.clarification_options, start=1):
            print(f"  {index}. {option}")

        raw_choice = input(
            f"\nSelect project intent [1-{len(result.clarification_options)}] (default: 1): "
        ).strip()
        selected_index = 1
        if raw_choice:
            try:
                selected_index = int(raw_choice)
            except ValueError:
                selected_index = 1

        if not 1 <= selected_index <= len(result.clarification_options):
            selected_index = 1

        self.config["project_intent_override"] = result.clarification_options[selected_index - 1]

    def _generate_yaml(self) -> None:
        platforms = list(self.config["target_platforms"])
        include_sections = list(self.config.get("include_sections", []))
        confirmed_skill_source = self.config["confirmed_skill_source"]
        fallback_sources = list(self.config.get("fallback_skill_sources", []))

        platforms_yaml = "\n".join(f"  - {platform}" for platform in platforms)
        sections_yaml = "\n".join(
            [
                "    - project-identity",
                "    - coding-standards",
                "    - critical-rules",
                "    - important-guidelines",
                "    - code-smells",
                "    - testing",
                *[f"    - {section}" for section in include_sections],
            ]
        )

        skill_sources_block = self._build_skill_sources_block(confirmed_skill_source, fallback_sources)

        yaml_content = (
            "# .rulesrc.yaml generated by Interactive Wizard\n"
            "target_platforms:\n"
            f"{platforms_yaml}\n\n"
            f"severity_level: {self.config['severity_level']}\n"
            f"output_language: {self.config['output_language']}\n\n"
            "sections:\n"
            "  include:\n"
            f"{sections_yaml}\n"
            "  exclude: []\n"
            f"{skill_sources_block}\n"
            f"template_style: {self.config['template_style']}\n"
            f"quality_threshold: {self.config['quality_threshold']}\n"
            f"confidence_threshold: {self.config['confidence_threshold']}\n"
            f"skill_match_limit: {self.config['skill_match_limit']}\n"
            f"agentic_match_limit: {self.config.get('agentic_match_limit', 3)}\n"
            f"project_intent_override: {self.config.get('project_intent_override', '')}\n"
            f"preview_mode: {'true' if self.config['preview_mode'] else 'false'}\n"
            "logging:\n"
            "  enabled: true\n"
            "  directory: .agent/logs\n"
            "memory:\n"
            "  enabled: true\n"
            "  summary_path: .agent/memory/project_state.md\n"
            "existing_files: ask\n"
        )
        Path(".rulesrc.yaml").write_text(yaml_content, encoding="utf-8")

    def _build_skill_sources_block(
        self,
        confirmed_skill_source: SkillSourceConfig,
        fallback_sources: list[SkillSourceConfig],
    ) -> str:
        lines = [
            "",
            "skill_sources:",
            f"  - path: {format_yaml_path(confirmed_skill_source.path)}",
        ]
        if confirmed_skill_source.format:
            lines.append(f"    format: {confirmed_skill_source.format}")
        lines.append("    confirmed: true")

        for source in fallback_sources:
            lines.append(f"  - path: {format_yaml_path(source.path)}")
            if source.format:
                lines.append(f"    format: {source.format}")
            lines.append("    confirmed: false")

        return "\n".join(lines)


def main() -> None:
    wizard = ConfigWizard()
    wizard.run()


if __name__ == "__main__":
    main()
