<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/naravid19/ai-project-rules-generator">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">AI Project Rules Generator</h3>

  <p align="center">
    🚀 Workflow for generating .cursorrules and AGENTS.md files with dynamic AI skills integration
    <br />
    <a href="#usage"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#example-output">View Example</a>
    &middot;
    <a href="https://github.com/naravid19/ai-project-rules-generator/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/naravid19/ai-project-rules-generator/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#key-features">Key Features</a></li>
        <li><a href="#supported-project-types">Supported Project Types</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#workflow-stages">Workflow Stages</a></li>
    <li><a href="#example-output">Example Output</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

A structured 5-stage workflow for creating professional project rules (`.cursorrules`) and AI agent guidelines (`AGENTS.md`). This workflow helps you establish consistent coding standards across all your projects while ensuring AI assistants understand your codebase.

### Why Use This?

- ✅ **Consistent Standards** - Same structure across all projects
- ✅ **AI-Ready** - AI assistants understand your codebase better
- ✅ **Dynamic Skills** - Never outdated with dynamic skill discovery
- ✅ **Time-Saving** - Complete in 30-60 minutes
- ✅ **Best Practices** - Built from proven patterns

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Key Features

| Feature              | Description                            |
| -------------------- | -------------------------------------- |
| **5-Stage Workflow** | Structured process with time estimates |
| **Keyword Tables**   | Easy skill discovery by project type   |

| **Verification Checklist** | Ensure quality with reader testing |
| **Quick Reference Card** | At-a-glance summary for fast execution |

### Supported Project Types

- 🌐 **Web Frontend** - React, Vue, Angular, Next.js
- ⚙️ **Backend API** - Node.js, Python, Go, Rust
- 🧩 **Chrome Extensions** - Manifest V3
- 📱 **Mobile Apps** - React Native, Flutter
- 💻 **CLI Tools** - Bash, PowerShell
- 🤖 **AI/ML Projects** - LLM, RAG, Agents
- 🎮 **Game Development** - Unity, Godot, Unreal

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

- An AI assistant that supports skills (Cursor, Claude, etc.)
- Access to `.agent/skills/CATALOG.md` (skill library)
- Your project source code

### Installation

1. Download the workflow file to your project:
   ```sh
   curl -o .agent/workflows/create-project-rules.md https://raw.githubusercontent.com/naravid19/ai-project-rules-generator/main/workflows/create-project-rules.md
   ```
   _(Ensure you have an `.agent/workflows` directory first)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE -->

## Usage

### Quick Start

Run the workflow with your AI assistant:

```
/create-project-rules
```

Or simply ask:

> "Create professional project rules for this project"

### Manual Execution

1. Open `.agent/workflows/create-project-rules.md`
2. Follow the 5 stages step by step
3. Get `.cursorrules` and `AGENTS.md` tailored to your project

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- WORKFLOW STAGES -->

## Workflow Stages

```
┌─────────────────────────────────────────────────────────┐
│           CREATE PROJECT RULES - QUICK REF              │
├─────────────────────────────────────────────────────────┤
│ Stage 1: Analyze         │ Config, Tech Stack, Patterns │
│ Stage 2: Skills          │ Search CATALOG.md + Read     │
│ Stage 3: .cursorrules    │ Standards, Rules, Examples   │
│ Stage 4: AGENTS.md       │ Skills section (dynamic!)    │
│ Stage 5: Verify          │ Checklist + Reader Test      │
├─────────────────────────────────────────────────────────┤
│ ⏱️  Total Time: 30-60 minutes                           │
└─────────────────────────────────────────────────────────┘
```

| Stage                      | Time      | Description                                |
| -------------------------- | --------- | ------------------------------------------ |
| **1. Project Analysis**    | 10-15 min | Understand structure, tech stack, patterns |
| **2. Skill Discovery**     | 5-10 min  | Search CATALOG.md for relevant skills      |
| **3. Create .cursorrules** | 10-20 min | Write coding standards and rules           |
| **4. Create AGENTS.md**    | 5-10 min  | Write AI guidelines with dynamic skills    |
| **5. Verification**        | 5 min     | Checklist and reader testing               |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- EXAMPLE OUTPUT -->

## Example Output

### .cursorrules (excerpt)

```markdown
# Project Rules: My Chrome Extension

## Tech Stack

- Language: JavaScript (ES2020+)
- Platform: Chrome Extension (Manifest V3)

## Critical Rules

1. ❌ Never use `localStorage` - use `chrome.storage` instead
2. ✅ Always check `chrome.runtime.lastError` after API calls
```

### AGENTS.md (excerpt)

```markdown
## 🎯 Available Skills

> [!IMPORTANT]
> Always check `.agent/skills/CATALOG.md` before starting any task!

### Helpful Keywords

- Extension: `browser`, `extension`, `chrome`, `manifest`
- Testing: `testing`, `jest`, `unit`
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [x] Core workflow with 5 stages
- [x] Time estimates for each stage
- [x] Example outputs
- [x] Quick reference card
- [ ] Add more project type examples
- [ ] Visual diagram for workflow
- [ ] Multi-language support

See the [open issues](https://github.com/naravid19/ai-project-rules-generator/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

naravid19 - [GitHub Profile](https://github.com/naravid19)

Project Link: [https://github.com/naravid19/ai-project-rules-generator](https://github.com/naravid19/ai-project-rules-generator)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

- [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
- [Cursor IDE](https://cursor.sh)
- [Anthropic Claude](https://anthropic.com)
- [Img Shields](https://shields.io)
- [Antigravity](https://deepmind.google/technologies/gemini/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/naravid19/ai-project-rules-generator.svg?style=for-the-badge
[contributors-url]: https://github.com/naravid19/ai-project-rules-generator/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/naravid19/ai-project-rules-generator.svg?style=for-the-badge
[forks-url]: https://github.com/naravid19/ai-project-rules-generator/network/members
[stars-shield]: https://img.shields.io/github/stars/naravid19/ai-project-rules-generator.svg?style=for-the-badge
[stars-url]: https://github.com/naravid19/ai-project-rules-generator/stargazers
[issues-shield]: https://img.shields.io/github/issues/naravid19/ai-project-rules-generator.svg?style=for-the-badge
[issues-url]: https://github.com/naravid19/ai-project-rules-generator/issues
[license-shield]: https://img.shields.io/github/license/naravid19/ai-project-rules-generator.svg?style=for-the-badge
[license-url]: https://github.com/naravid19/ai-project-rules-generator/blob/master/LICENSE
