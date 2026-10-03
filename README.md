# DoubleAgent

Learn to build production-ready agentic AI applications in Python by building one yourself:
a procurement assistant agent for a fictional company, Acme Industrial.

The path follows the 8 modules of the Reference *AI Agents for Enterprises* syllabus, Python track.
It is built on the Anthropic Python SDK (Claude), then LangChain, LangGraph, Semantic Kernel,
LangSmith and Langfuse. Every concept is compared with its C# equivalent.

| Start here | |
|---|---|
| [docs/SETUP.md](docs/SETUP.md) | Install uv, open in VS Code, run the checks |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Modules, lessons and deliverables |
| [docs/PYTHON_CONCEPTS.md](docs/PYTHON_CONCEPTS.md) | Which Python features and stdlib modules each lesson teaches |
| [Lesson 1.1](docs/lessons/module-01/1.1-setup-and-first-call.md) | Current lesson |

## How it works

The code in `src/doubleagent/` contains stubs (`raise NotImplementedError`) with TODOs.
The tests in `tests/` define "done". Implement until everything is green:

```bash
uv run ruff format . && uv run ruff check . && uv run pyright && uv run pytest -q
```

(or **Ctrl+Shift+B** in VS Code). Then push and ask for a review in the project thread.
