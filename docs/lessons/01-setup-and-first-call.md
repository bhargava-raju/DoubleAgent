# Lesson 1: Project setup and your first LLM call

**Goal:** a typed, tested Python project that sends a question to Claude and prints
the answer: `uv run doubleagent "What is an AI agent?"`

**You'll learn:** uv and `pyproject.toml`, the `src/` layout, type hints, `async`/`await`,
typed configuration with pydantic-settings, the Messages API, and testing with a fake client.

---

## 1. Concepts

### 1.1 uv and `pyproject.toml` (≈ dotnet CLI + `.csproj` + NuGet)

| C# / .NET | Python (modern) |
|-----------|-----------------|
| `dotnet` CLI | `uv` (installs Python, creates envs, manages deps, runs things) |
| `.csproj` | `pyproject.toml` |
| NuGet `PackageReference` | `[project] dependencies` |
| `packages.lock.json` | `uv.lock` (commit it) |
| `bin/obj` per project | `.venv/` (an isolated interpreter + packages; never commit it) |
| `dotnet run` | `uv run <command>` (auto-syncs deps, runs inside `.venv`) |
| Dev-only packages (test SDK) | `[dependency-groups] dev = [...]` via `uv add --dev` |

Forget `pip install` into your global Python. `uv add x` updates `pyproject.toml`,
the lock file and `.venv` in one step, like `dotnet add package`.

### 1.2 Modules and packages (≈ namespaces + assemblies)

- A **module** is one `.py` file. A **package** is a folder with `__init__.py`.
- `from doubleagent.config import Settings` ≈ `using DoubleAgent.Config;` but you import
  *names*, not whole namespaces.
- We use the **`src/` layout** (`src/doubleagent/...`) so tests import the installed
  package, not stray files. Think "the project is built and referenced", not "files on disk".

### 1.3 Type hints (≈ static types, but checked by a separate tool)

```python
def add(a: int, b: int) -> int: ...
name: str | None = None          # C#: string? name = null;
items: list[str] = []            # C#: List<string>
```

Python **does not enforce** these at runtime. A type checker (**pyright**, the same engine
as VS Code's Pylance) enforces them, like the C# compiler would. We run it in CI-style checks.
Pydantic is the exception: it *does* validate at runtime, which is why we use it at boundaries.

### 1.4 `async`/`await` (≈ `Task`, almost identical)

```python
async def get_answer() -> str:        # C#: async Task<string> GetAnswerAsync()
    return await client.call()

asyncio.run(main())                    # C#: the async Main entry point
```

Differences that bite C# devs:
- Calling an `async def` without `await` gives you a coroutine object, not a running task.
  Nothing happens until it's awaited. (C# Tasks are hot; Python coroutines are cold.)
- There's one event loop per thread, started by `asyncio.run(...)` at the top of the program.
- `async with` ≈ `await using`: it disposes async resources like HTTP clients.

LLM calls are slow network I/O, so production AI code is async by default.

### 1.5 Configuration with pydantic-settings (≈ `IOptions<T>` + `appsettings.json`)

```python
class Settings(BaseSettings):
    anthropic_api_key: SecretStr     # read from env var ANTHROPIC_API_KEY or .env
    model: str = "claude-opus-5-5"
```

Fields bind from environment variables (case-insensitive) or a `.env` file, and are validated.
`SecretStr` hides the value in logs and `repr` (call `.get_secret_value()` to use it).
Missing required values fail fast at startup, like options validation in .NET.

### 1.6 The Messages API (the one call everything else builds on)

An LLM call is: **model + messages (+ system prompt, tools, limits) → response content blocks**.

```python
response = await client.messages.create(
    model="claude-opus-5-5",
    max_tokens=16000,
    messages=[{"role": "user", "content": "Hello"}],
)
```

- `messages` is the whole conversation so far. The API is **stateless**: you resend history every call.
- `response.content` is a **list of blocks** (`text`, `thinking`, later `tool_use`). Filter to `type == "text"`
  for the answer. Current models think before answering, so you will see non-text blocks.
- `response.stop_reason` tells you *why* it stopped (`end_turn`, `max_tokens`, `tool_use`, `refusal`).
  In Lesson 3 this becomes the heartbeat of the agent loop.
- `response.usage` gives input/output token counts, which is what you pay for.
- Tokens ≈ ¾ of a word. `max_tokens` caps the *output*; too low and answers get cut off.

### 1.7 Testing with a fake (≈ an interface + a test double)

Pass the client into your function instead of creating it inside (dependency injection).
Python has no need for an `IAnthropicClient` interface: any object with the right
methods works ("duck typing"). In tests, pass a small fake object; no network, no cost.

---

## 2. Exercise

Do these yourself. Commit after each step. Stuck for more than 15 minutes? Ask in the thread
for a hint (not the answer).

### Step 1: Create the project

You need an API key from <https://console.anthropic.com> (Settings → API Keys).

```bash
# Install uv: https://docs.astral.sh/uv/getting-started/installation/
cd DoubleAgent
uv init --package --python 3.13 .     # creates pyproject.toml and src/doubleagent/
uv add anthropic pydantic-settings
uv add --dev pytest pytest-asyncio ruff pyright
```

Then:
1. Open `pyproject.toml` and read every section. Match each to the table in 1.1.
2. Add test and lint settings to `pyproject.toml`:
   ```toml
   [tool.pytest.ini_options]
   asyncio_mode = "auto"   # lets pytest run `async def test_...` functions

   [tool.ruff.lint]
   select = ["E", "F", "I", "UP", "B"]
   ```
3. Create `.env` with `ANTHROPIC_API_KEY=sk-ant-...` (already in `.gitignore`; never commit it).
4. Point VS Code (or Rider) at `.venv` as the interpreter.

### Step 2: `src/doubleagent/config.py`

Write a `Settings` class (see 1.5) with:
- `anthropic_api_key` (secret, required)
- `model` defaulting to `"claude-opus-5-5"`
- `max_tokens` defaulting to `16000`
- reads from `.env`, ignoring unknown variables (look up `SettingsConfigDict`)

Add `get_settings() -> Settings` that returns a cached instance.
Hint: `functools.lru_cache` ≈ a lazy singleton.

### Step 3: `src/doubleagent/chat.py`

```python
async def ask(client: AsyncAnthropic, model: str, max_tokens: int, question: str) -> str:
    """Send one question to Claude and return only the text of the answer."""
```

- Await `client.messages.create(...)`.
- Join the `.text` of every block whose `.type == "text"`.
- Bonus: if `stop_reason == "max_tokens"`, log or raise something useful.

### Step 4: The CLI entry point

`uv init --package` created a `main()` in `src/doubleagent/__init__.py`, wired up under
`[project.scripts]` in `pyproject.toml` (≈ the `Main` method). Make it:
1. Read the question from `sys.argv[1:]` (≈ `args`).
2. Load settings, create an `AsyncAnthropic` client inside `async with`, call `ask`, print the result.
3. Use `asyncio.run(...)` to bridge from sync `main()` into async code.

```bash
uv run doubleagent "Explain an AI agent to a C# developer in 3 sentences"
```

### Step 5: Test it without the network: `tests/test_chat.py`

Write `async def test_ask_returns_text()` that:
- builds a fake object whose `.messages.create(**kwargs)` is an `async def` returning something with
  `.content = [<object with .type="text" and .text="Paris">]`
  (hint: `types.SimpleNamespace` makes throwaway objects quickly),
- asserts `ask(...)` returns `"Paris"`,
- asserts the question was sent as the user message.

Add a second test where the fake returns a `thinking` block *and* a `text` block, and check only the text comes back.

### Step 6: The quality gate

All three must pass before you call the lesson done (this is what CI will run in Lesson 12):

```bash
uv run ruff format . && uv run ruff check .
uv run pyright
uv run pytest -q
```

---

## 3. Check yourself

- Why does `ask` take the client as a parameter instead of creating one?
- What happens if you call `ask(...)` without `await`?
- What's in `response.usage` for your CLI call, and what would 1,000 such calls cost?
  (Prices: <https://www.anthropic.com/pricing>.)
- Why is `.env` in `.gitignore` but `uv.lock` is committed?

When done, push your branch and say "Lesson 1 done" in the thread. I'll review your code
and we'll move on to **Lesson 2: Structured outputs**.
