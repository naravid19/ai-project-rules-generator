# 📋 Template Gallery

Pre-made `.cursorrules` examples for common project types. Use these as **references** — the workflow generates custom versions tailored to your project.

## Available Templates

| Template               | Directory           | Best For                                  |
| ---------------------- | ------------------- | ----------------------------------------- |
| **React + TypeScript** | `react-typescript/` | React SPAs, Next.js, Vite projects        |
| **Python FastAPI**     | `python-fastapi/`   | REST APIs, microservices, async backends  |
| **Flutter Mobile**     | `flutter-mobile/`   | Cross-platform mobile apps                |
| **Node.js Express**    | `nodejs-express/`   | Express.js REST APIs, TypeScript backends |
| **Chrome Extension**   | `chrome-extension/` | Manifest V3 browser extensions            |
| **Next.js Full-Stack** | `nextjs-fullstack/` | Full-stack web apps with App Router       |
| **Go Microservice**    | `go-microservice/`  | Cloud-native Go services, Kubernetes      |
| **Unity Game**         | `unity-game/`       | 3D/2D games with C# and Unity             |
| **CLI Tool**           | `cli-tool/`         | Command-line tools with Commander.js      |
| **LangChain RAG**      | `langchain-rag/`    | AI/ML RAG pipelines, LLM applications     |

## Configuration Template

| File                    | Purpose                                                      |
| ----------------------- | ------------------------------------------------------------ |
| `rulesrc-template.yaml` | Example `.rulesrc.yaml` config — customize workflow behavior |

## How to Use

These templates are **NOT** meant to be copied directly. Instead:

1. **Run the workflow** — `/create-project-rules` generates tailored files
2. **Use templates as inspiration** — compare your generated files with these
3. **Configure with `.rulesrc.yaml`** — copy `rulesrc-template.yaml` to your project root as `.rulesrc.yaml`
4. **Contribute your own** — submit a PR with your project type template

> [!TIP]
> The workflow will generate better results than any template because it analyzes YOUR specific project.

## Template Structure

Each template directory contains:

```
{project-type}/
└── .cursorrules    # Example coding standards
```

## Coverage by Category

| Category             | Templates                                        |
| -------------------- | ------------------------------------------------ |
| 🌐 Web Frontend      | React TypeScript, Next.js Full-Stack             |
| ⚙️ Backend API       | Python FastAPI, Node.js Express, Go Microservice |
| 🧩 Browser Extension | Chrome Extension                                 |
| 📱 Mobile App        | Flutter Mobile                                   |
| 🎮 Game Dev          | Unity Game                                       |
| 💻 CLI Tool          | CLI Tool                                         |
| 🤖 AI/ML             | LangChain RAG                                    |
