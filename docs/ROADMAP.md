# Roadmap

**What we're building:** DoubleAgent, a research assistant agent that can answer
questions by calling tools (search your notes, fetch web pages, run calculations),
remember context, and be served over an HTTP API. Each lesson adds one layer.

**Stack:** Python 3.13, [uv](https://docs.astral.sh/uv/), Anthropic Python SDK
(Claude), Pydantic v2, pytest, ruff, pyright, FastAPI, OpenTelemetry, Docker.

We start *without* an agent framework so you understand what one does for you,
then adopt the SDK's helpers once the mechanics are clear.

| # | Lesson | Agentic concept | Python concepts |
|---|--------|-----------------|-----------------|
| 1 | Project setup and first LLM call | Messages API, models, tokens | uv, `pyproject.toml`, packages/modules, type hints, `async`/`await`, pydantic-settings, pytest |
| 2 | Structured outputs | Getting typed JSON back from an LLM | Pydantic models, validation, `Literal`, enums |
| 3 | Tools and the agent loop | Tool use, the think-act-observe loop, stop reasons | functions as values, dicts, JSON Schema, `match` |
| 4 | Streaming and the SDK tool runner | Streaming tokens, letting the SDK drive the loop | async iterators, decorators, context managers |
| 5 | Conversation memory and context | Multi-turn state, prompt caching, context limits | dataclasses vs Pydantic, protocols |
| 6 | Retrieval (RAG) as a tool | Embeddings/search, grounding, citations | file I/O, `pathlib`, generators |
| 7 | MCP | Consuming and exposing tools via Model Context Protocol | packaging, entry points |
| 8 | Workflow patterns and multi-agent | Routing, orchestrator-workers, evaluator-optimizer | `asyncio.gather`, task groups, cancellation |
| 9 | Evals and testing | Building an eval set, LLM-as-judge, regression tests | pytest fixtures, parametrize, mocks |
| 10 | Guardrails, errors, and cost | Refusals, retries, rate limits, token budgets | exceptions, `tenacity`-style retries, logging |
| 11 | Observability | Tracing agent runs and tool calls | OpenTelemetry, structured logging |
| 12 | Ship it | HTTP API with streaming, containerize, CI | FastAPI, SSE, Docker, GitHub Actions |

Order may shift based on your questions. Each lesson lives in `docs/lessons/`.
