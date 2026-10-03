# Setup: Python + VS Code

## 1. Install the tools

| Tool | Install | C# equivalent |
|------|---------|---------------|
| uv | <https://docs.astral.sh/uv/getting-started/installation/> (Windows: `winget install astral-sh.uv`) | the `dotnet` CLI |
| Python 3.13 | `uv python install 3.13` (uv manages Python versions for you) | the .NET SDK |
| VS Code | <https://code.visualstudio.com> | Visual Studio / Rider |
| Git | <https://git-scm.com> | |

You do not need a system-wide Python or `pip`.

## 2. Get the code and dependencies

```bash
git clone https://github.com/bhargava-raju/DoubleAgent.git
cd DoubleAgent
git checkout claude/project-thread-qjq7wy
uv sync                      # creates .venv and installs exact versions from uv.lock
cp .env.example .env         # then put your Anthropic API key in .env
code .
```

`uv sync` ≈ `dotnet restore`. Re-run it whenever `pyproject.toml` or `uv.lock` changes.

## 3. VS Code

When VS Code opens the folder, accept **"Install recommended extensions"** (from `.vscode/extensions.json`):

| Extension | What it gives you |
|-----------|-------------------|
| Python + Pylance | IntelliSense, go-to-definition, type checking as you type (Pylance = pyright) |
| Python Debugger (debugpy) | F5 debugging with breakpoints |
| Ruff | format on save, lint squiggles, organize imports |
| Even Better TOML | `pyproject.toml` highlighting and validation |
| DotENV | `.env` highlighting |

Then check the bottom-right status bar shows the interpreter **`.venv`**.
If it doesn't: `Ctrl+Shift+P` → **Python: Select Interpreter** → pick `./.venv`.

What's preconfigured in `.vscode/`:

| File | Use it for | C# equivalent |
|------|-----------|---------------|
| `settings.json` | format on save, pytest in Test Explorer, inlay type hints | `.editorconfig` + IDE settings |
| `launch.json` | **F5** to debug `ask`, `agent`, `compare`, or the current test file | `launchSettings.json` |
| `tasks.json` | **Ctrl+Shift+B** runs format + lint + types + tests | `dotnet build && dotnet test` |

Test Explorer (the flask icon) discovers everything under `tests/`. Click ▶ to run, or the bug icon to debug a single test.

## 4. The quality gate

Every lesson is "done" when all of these pass (also bound to Ctrl+Shift+B):

```bash
uv run ruff format .      # formatter      (dotnet format)
uv run ruff check .       # linter         (Roslyn analyzers)
uv run pyright            # type checker   (the C# compiler's type checks)
uv run pytest -q          # tests          (dotnet test)
```

`uv run <cmd>` runs a command inside `.venv` without activating it. In VS Code's terminal the venv is
activated for you, so plain `pytest` or `python` also work there.

## 5. Running the app

```bash
uv run doubleagent ask "What is an AI agent?"
uv run doubleagent agent "Can we order hydraulics from Globex?"
uv run doubleagent compare
```

These raise `NotImplementedError` until you complete the Module 1 exercises.
