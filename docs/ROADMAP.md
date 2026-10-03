# Roadmap

This path follows the 8 modules of the *Vizuara: AI Agents for Enterprises* syllabus,
using the **Python track throughout** (no n8n) with a coding exercise in every lesson.

## What you're building

**DoubleAgent**, a procurement assistant for a fictional company, *Acme Industrial*.
It answers questions from approved policy documents, looks up and onboards suppliers
in a sample "headless ERP", prepares purchase requests, and never writes to the ERP
without a human approval. By the end it is evaluated, traced, durable, and deployable.

This is the syllabus's running example, so every module adds one layer to the same app.

**Approach:** each concept is first built directly on the **Anthropic Python SDK**, so you see exactly what
goes over the wire, then rebuilt with **LangChain / LangGraph** and **Semantic Kernel** so you can judge what
each framework adds. Tracing and evals use **LangSmith** and **Langfuse**.

## Stack

| Concern | Choice | C# mental model |
|---------|--------|-----------------|
| Project/deps | `uv`, `pyproject.toml` | dotnet CLI, `.csproj`, NuGet |
| LLM | Claude via the official Anthropic Python SDK (`anthropic`), the foundation of every module | an SDK client like `HttpClient` wrappers |
| Data contracts | Pydantic v2 | records + DataAnnotations, validated at runtime |
| Tests / lint / types | pytest, ruff, pyright | xUnit, analyzers, the compiler |
| Retrieval | embeddings + BM25 (hybrid), Markdown "LLM Wiki" | Azure AI Search / Lucene |
| Tools | FastAPI (sample ERP), `httpx`, MCP Python SDK | ASP.NET Core minimal APIs, `HttpClient` |
| Agent frameworks | LangChain (`langchain-anthropic`), Semantic Kernel (Python, Anthropic connector), both running Claude | Semantic Kernel for .NET (same concepts) |
| Orchestration | LangGraph (primary), Semantic Kernel agents/processes (comparison) | a state machine / Durable Functions orchestrator |
| Eval + tracing | LangSmith and Langfuse (OpenTelemetry) | Application Insights |
| Durable execution | Temporal | Durable Functions / MassTransit sagas |
| Ship | FastAPI + Docker + GitHub Actions | ASP.NET Core + Docker + Azure DevOps |

## How each lesson works

1. Read the lesson in `docs/lessons/` (concepts first, with C# comparisons).
2. The repo has **stubs** (`raise NotImplementedError`) and **tests that define "done"**.
3. You implement the stubs until `uv run pytest tests/<module>` is green, plus ruff and pyright.
4. Each lesson's **Pillars** section covers orchestration, context, guardrails, security, evaluation,
   observability, performance and reliability for that step.
5. Each module ends with the syllabus **deliverable**. Push and ask for a review in the thread.

## The eight pillars, at every stage

A demo agent works on the happy path. A production agent is defined by everything around it.
Every module and every lesson has a **Pillars** section showing where each of these appears in that step,
what to notice, and usually something to build or measure.

| Pillar | Question it answers | C# mental model |
|--------|--------------------|-----------------|
| 🧭 **Orchestration** | Who decides the next step (code, model, graph, human), and how is state carried? | pipelines, state machines, sagas |
| 🧠 **Context & memory** | What does the model see on each call, and what's remembered between calls? | request scope vs session vs database |
| 🛡️ **Guardrails** | What must never happen, and what stops it? Validation, scope limits, budgets, approvals | validation, authorization policies |
| 🔐 **Security & privacy** | Prompt injection, least-privilege tools, secrets, PII, data residency and retention | OWASP, managed identities, data protection |
| 📏 **Evaluation** | How do we know it's right, and that it stays right after changes? | unit/integration tests, acceptance criteria |
| 🔭 **Observability** | Can we see why a run did what it did? Traces, logs, token and tool records | Application Insights, structured logging |
| ⚡ **Performance & cost** | Latency, tokens, dollars per task, throughput, caching, model choice | profiling, caching, `Task.WhenAll` |
| 🔁 **Reliability** | Timeouts, retries, idempotency, durable state, recovery, graceful degradation | Polly, outbox pattern, Durable Functions |

## Modules

### Module 1: LLM foundations → your first agent
Tokens, context windows, prompting, hallucinations; chatbot vs workflow vs agent; model trade-offs.
- 1.1 Project setup and your first LLM call
- 1.2 Chatbot vs workflow vs agent: build the agent loop by hand (supplier lookup tool)
- 1.3 Model comparison scorecard: quality, latency, cost across Claude models
- 1.4 The same agent in LangChain and in Semantic Kernel: what frameworks do for you, and what they hide

**Deliverable:** a working first agent (hand-built, LangChain, Semantic Kernel) and a model-comparison scorecard.

| Pillar | In this module |
|---|---|
| 🧭 Orchestration | Chatbot vs workflow vs agent; the hand-written tool loop; then LangChain and Semantic Kernel agents |
| 🧠 Context & memory | Stateless API: you resend history; context windows; what thinking and tool blocks add to it |
| 🛡️ Guardrails | Validated settings, `max_tokens`/`stop_reason` checks, tool input validation, `max_turns` |
| 🔐 Security & privacy | Secrets out of code (`SecretStr`, `.env`); first prompt-injection probe; a read-only tool |
| 📏 Evaluation | Specs with a fake client; first quality metric (keywords) in the scorecard |
| 🔭 Observability | Logging every tool call; `usage` per call |
| ⚡ Performance & cost | Tokens and dollars per call, latency, concurrent calls, parallel tool calls, model tier choice |
| 🔁 Reliability | SDK timeouts and automatic retries; tool errors returned to the model instead of crashing |

### Module 2: Enterprise context: RAG + LLM Wiki
- 2.1 Chunking and embeddings; vector search (by hand, then LangChain document loaders, splitters, vector stores)
- 2.2 Hybrid retrieval (BM25 + vectors) with LangChain retrievers; answers with source citations
- 2.3 LLM Wiki: linked Markdown pages and index-based, vectorless retrieval; compare with RAG
- 2.4 Freshness, contradictory sources, and access boundaries (live data stays in the ERP)

**Deliverable:** a source-linked knowledge assistant and a retrieval comparison worksheet.

| Pillar | In this module |
|---|---|
| 🧭 Orchestration | Retrieval as a fixed step (workflow) vs retrieval as a tool (agent) |
| 🧠 Context & memory | Chunking, context budgets, what to retrieve vs what to keep in the ERP (live data) |
| 🛡️ Guardrails | Answer only from sources; refuse or flag when sources conflict or are stale |
| 🔐 Security & privacy | Document-level access boundaries; no leaking restricted chunks; injection hidden in documents |
| 📏 Evaluation | Retrieval metrics (hit rate, MRR), citation correctness, the retrieval comparison worksheet |
| 🔭 Observability | Logging which chunks were retrieved and cited |
| ⚡ Performance & cost | Chunk size vs recall, embedding cost, prompt caching for long context |
| 🔁 Reliability | Index freshness, re-indexing, fallback when the vector store is down |

### Module 3: Tools, APIs + Model Context Protocol
- 3.1 The sample ERP as a FastAPI service; calling it with `httpx`
- 3.2 Tool inputs and structured outputs with Pydantic; timeouts and retries
- 3.3 Idempotency keys: preventing duplicate writes
- 3.4 MCP: expose scoped tools; the model suggests, the service authorizes
- 3.5 Consuming MCP tools from LangChain (`langchain-mcp-adapters`) and Semantic Kernel plugins

**Deliverable:** supplier lookup and request-creation tools with explicit permissions.

| Pillar | In this module |
|---|---|
| 🧭 Orchestration | Tools behind an API and MCP; choosing among many tools |
| 🧠 Context & memory | Compact tool results; what to return to the model vs keep server-side |
| 🛡️ Guardrails | Pydantic input validation, structured outputs, explicit permissions per tool |
| 🔐 Security & privacy | The model suggests, the service authorizes; least privilege; MCP authorization scopes |
| 📏 Evaluation | Tool-call correctness tests: right tool, right arguments, right refusal |
| 🔭 Observability | Request ids correlated across agent and service logs |
| ⚡ Performance & cost | Connection reuse, parallel calls, fewer round trips |
| 🔁 Reliability | Timeouts, retries with backoff, idempotency keys so retries never duplicate writes |

### Module 4: Orchestration with LangGraph (and Semantic Kernel)
- 4.1 Workflows as state + transitions in LangGraph; nodes, edges, typed state, reducers
- 4.2 Specialist roles and routing; confidence-based escalation vs an LLM-router baseline
- 4.3 Checkpointing and resuming; one agent vs multiple agents (supervisor pattern)
- 4.4 The same workflow with Semantic Kernel agent orchestration; when to pick which

**Deliverable:** a resumable workflow and a routing evaluation that includes uncertain cases.
(The syllabus also covers Jev from TypeSafe, which is early access; we use recorded fixtures if available.)

| Pillar | In this module |
|---|---|
| 🧭 Orchestration | LangGraph state, nodes, edges, routing, checkpoints; Semantic Kernel orchestration; one vs many agents |
| 🧠 Context & memory | Typed graph state, reducers, what each specialist sees vs shared state |
| 🛡️ Guardrails | Confidence thresholds and escalation, recursion limits, bounded loops |
| 🔐 Security & privacy | Per-agent tool scopes; isolating untrusted content between agents |
| 📏 Evaluation | Routing evaluation including uncertain cases; single vs multi-agent comparison |
| 🔭 Observability | Visualizing the graph; per-node traces |
| ⚡ Performance & cost | Cheap router + strong worker, fan-out, cost of extra agents |
| 🔁 Reliability | Checkpoint and resume after a crash |

### Module 5: Headless ERP + human approvals
- 5.1 Supplier onboarding and purchase-request preparation
- 5.2 Human-in-the-loop with LangGraph `interrupt()` and resume; approvals tied to a proposal version
- 5.3 Failure drills: missing documents, duplicate suppliers, prompt injection, a lost ERP response

**Deliverable:** an approval-gated supplier workflow with a readable activity record.

| Pillar | In this module |
|---|---|
| 🧭 Orchestration | Human-in-the-loop with `interrupt()` and resume |
| 🧠 Context & memory | Proposal snapshots: what the approver saw is what gets executed |
| 🛡️ Guardrails | Approval gates tied to a proposal version; duplicate-supplier and missing-document checks |
| 🔐 Security & privacy | Prompt injection in supplier documents; separation of duties; audit trail |
| 📏 Evaluation | Failure drills as automated tests |
| 🔭 Observability | A readable activity record for every decision |
| ⚡ Performance & cost | Waiting for humans without holding resources |
| 🔁 Reliability | A lost ERP response: check before retrying the write |

### Module 6: Evaluation + observability with LangSmith and Langfuse
- 6.1 Test sets: normal, edge, and adversarial cases; success in business terms
- 6.2 Tracing LangChain/LangGraph runs in LangSmith; datasets and experiments
- 6.3 The same traces and evals in Langfuse (open source, self-hostable); comparing the two
- 6.4 LLM-as-judge calibrated by human review; turning a failure into a regression test

**Deliverable:** an evaluation scorecard and a trace showing why a run succeeded or failed.

| Pillar | In this module |
|---|---|
| 🧭 Orchestration | Tracing whole graph runs step by step |
| 🧠 Context & memory | Spotting context bloat and wasted tokens in traces |
| 🛡️ Guardrails | Regression tests created from real failures |
| 🔐 Security & privacy | Adversarial and red-team test sets; PII in traces (masking) |
| 📏 Evaluation | LangSmith and Langfuse datasets, experiments, LLM-as-judge calibrated by human review |
| 🔭 Observability | LangSmith and Langfuse traces, OpenTelemetry |
| ⚡ Performance & cost | Cost and latency per run and per step; finding the slow node |
| 🔁 Reliability | Flaky-run analysis; comparing failure rates across versions |

### Module 7: Deploy + recover with Temporal
- 7.1 Temporal workflows and activities; long waits for approvals
- 7.2 Recovery: check receipts before retrying a write
- 7.3 FastAPI service in Docker; secrets, access control, budgets, monitoring, rollback

**Deliverable:** a shareable pilot, an operating checklist, and a recovery demonstration.

| Pillar | In this module |
|---|---|
| 🧭 Orchestration | Temporal workflows for durable, long-running orchestration |
| 🧠 Context & memory | Conversation and workflow state stored outside the process |
| 🛡️ Guardrails | Budgets (tokens, dollars, turns) enforced per run and per user |
| 🔐 Security & privacy | Secrets management, access control, an accountable owner |
| 📏 Evaluation | Smoke tests and production monitors with alerts |
| 🔭 Observability | Dashboards and alerts on cost, errors, latency |
| ⚡ Performance & cost | Concurrency and rate limits, autoscaling, batch vs real time |
| 🔁 Reliability | Recovery demo, receipts before retries, rollback plan |

### Module 8: Capstone: your domain pilot
Adapt DoubleAgent to a business task you know. Demo an approved action, a rejected action,
and a controlled failure with evaluation evidence; write the rollout proposal.

**Deliverable:** working pilot, short demo, realistic rollout proposal.

| Pillar | In this module |
|---|---|
| 🧭 Orchestration | Your domain workflow end to end |
| 🧠 Context & memory | What your domain's agent must know vs look up |
| 🛡️ Guardrails | An approved, a rejected and a controlled-failure demo |
| 🔐 Security & privacy | Your domain's data-handling and compliance constraints |
| 📏 Evaluation | Evaluation evidence in the pitch |
| 🔭 Observability | A trace walkthrough of one run |
| ⚡ Performance & cost | Cost and latency budget in the rollout proposal |
| 🔁 Reliability | Operating checklist and on-call plan |

## Python concepts

Every lesson deliberately uses specific language features and standard-library modules.
See [PYTHON_CONCEPTS.md](PYTHON_CONCEPTS.md) for the full map.
