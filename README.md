# DoubleAgent

Learn to build production-ready agentic AI applications in Python by building one yourself:
a procurement assistant agent for a fictional company, Acme Industrial.

The path follows the 8 modules of the Reference *AI Agents for Enterprises* syllabus, Python track.
It is built on the Anthropic Python SDK (Claude), then LangChain, LangGraph, Semantic Kernel,
LangSmith and Langfuse. Every module ends with a UI you can demo, and every concept is
compared with its C# equivalent.

| Start here | |
|---|---|
| [docs/SETUP.md](docs/SETUP.md) | Install uv, open in VS Code, run the checks |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Modules, lessons and deliverables |
| [docs/PYTHON_CONCEPTS.md](docs/PYTHON_CONCEPTS.md) | Which Python features and stdlib modules each lesson teaches |
| [Lesson 1.1](docs/lessons/module-01/1.1-setup-and-first-call.md) | Current lesson |

## How to use this repo

### Layout

```
src/doubleagent/   your code: stubs with TODOs (you write the bodies)
src/doubleagent/ui the UI (Streamlit now, FastAPI web front end in Module 7)
tests/moduleNN/    the spec: tests that define "done" for each module (don't edit them)
tests/fakes.py     fake Claude client so tests need no network or API key
data/erp/          sample ERP data (suppliers)
docs/lessons/      one lesson per step: concepts, exercise, Pillars, check-yourself
notes/             your experiment notes and answers (create it; it's yours)
.vscode/           debug profiles, test explorer, format on save, Ctrl+Shift+B gate
```

### One-time setup
Follow [docs/SETUP.md](docs/SETUP.md): install uv, `uv sync`, copy `.env.example` to `.env`, open in VS Code.

### The loop for every lesson

1. **Branch** off the latest learning branch: `git switch -c learn/1.1`
2. **Read** the lesson's *Concepts* section. Skim [PYTHON_CONCEPTS.md](docs/PYTHON_CONCEPTS.md) for new syntax.
3. **Read the tests first.** They're the spec, like acceptance criteria.
4. **Go red → green, one test at a time:**
   ```bash
   uv run pytest tests/module01/test_llm.py -x -q          # stop at the first failure
   uv run pytest -k "returns_text" -q                       # run one test by name
   ```
   Stuck? Set a breakpoint and use **Debug current test file** (F5) instead of guessing.
5. **Pass the quality gate** (Ctrl+Shift+B):
   `uv run ruff format . && uv run ruff check . && uv run pyright && uv run pytest -q`
6. **Run it for real** (`uv run doubleagent ...` or the Streamlit UI) and do the lesson's *Experiment*, writing findings in `notes/`.
7. **Work through the Pillars table.** These are the production habits; do at least the 🛡️ and 📏 rows.
8. **Answer "Check yourself"** in `notes/` without looking anything up.
9. **Commit and push** (`git push -u origin learn/1.1`), then post in the project thread:
   *"Lesson 1.1 done, branch learn/1.1"*. I review the code and notes, then the next lesson follows.

### Getting help without spoiling it
Ask in the thread with the level you want:
- **"hint"**: a nudge toward the idea
- **"bigger hint"**: the approach, or which API or function to use
- **"explain"**: the concept again, a different way
- **"review"**: feedback on code you've written

Solutions are never committed. Try for 15 minutes before asking.

### Tips
- **Save money while experimenting:** set `MODEL=claude-haiku-4-5` in `.env`; switch back for the scorecard.
  Tests never call the API.
- **Never commit `.env`.** `git status` should never list it.
- Hover over anything in VS Code to see its type; **F12** goes to the definition, including inside the
  Anthropic SDK. Reading SDK source is a great way to learn Python.
- Keep `notes/` honest: wrong guesses you corrected are the most useful notes later.
