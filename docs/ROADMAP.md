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
4. Each module ends with the syllabus **deliverable**. Push and ask for a review in the thread.

## Modules

### Module 1: LLM foundations → your first agent
Tokens, context windows, prompting, hallucinations; chatbot vs workflow vs agent; model trade-offs.
- 1.1 Project setup and your first LLM call
- 1.2 Chatbot vs workflow vs agent: build the agent loop by hand (supplier lookup tool)
- 1.3 Model comparison scorecard: quality, latency, cost across Claude models
- 1.4 The same agent in LangChain and in Semantic Kernel: what frameworks do for you, and what they hide

**Deliverable:** a working first agent (hand-built, LangChain, Semantic Kernel) and a model-comparison scorecard.

### Module 2: Enterprise context: RAG + LLM Wiki
- 2.1 Chunking and embeddings; vector search (by hand, then LangChain document loaders, splitters, vector stores)
- 2.2 Hybrid retrieval (BM25 + vectors) with LangChain retrievers; answers with source citations
- 2.3 LLM Wiki: linked Markdown pages and index-based, vectorless retrieval; compare with RAG
- 2.4 Freshness, contradictory sources, and access boundaries (live data stays in the ERP)

**Deliverable:** a source-linked knowledge assistant and a retrieval comparison worksheet.

### Module 3: Tools, APIs + Model Context Protocol
- 3.1 The sample ERP as a FastAPI service; calling it with `httpx`
- 3.2 Tool inputs and structured outputs with Pydantic; timeouts and retries
- 3.3 Idempotency keys: preventing duplicate writes
- 3.4 MCP: expose scoped tools; the model suggests, the service authorizes
- 3.5 Consuming MCP tools from LangChain (`langchain-mcp-adapters`) and Semantic Kernel plugins

**Deliverable:** supplier lookup and request-creation tools with explicit permissions.

### Module 4: Orchestration with LangGraph (and Semantic Kernel)
- 4.1 Workflows as state + transitions in LangGraph; nodes, edges, typed state, reducers
- 4.2 Specialist roles and routing; confidence-based escalation vs an LLM-router baseline
- 4.3 Checkpointing and resuming; one agent vs multiple agents (supervisor pattern)
- 4.4 The same workflow with Semantic Kernel agent orchestration; when to pick which

**Deliverable:** a resumable workflow and a routing evaluation that includes uncertain cases.
(The syllabus also covers Jev from TypeSafe, which is early access; we use recorded fixtures if available.)

### Module 5: Headless ERP + human approvals
- 5.1 Supplier onboarding and purchase-request preparation
- 5.2 Human-in-the-loop with LangGraph `interrupt()` and resume; approvals tied to a proposal version
- 5.3 Failure drills: missing documents, duplicate suppliers, prompt injection, a lost ERP response

**Deliverable:** an approval-gated supplier workflow with a readable activity record.

### Module 6: Evaluation + observability with LangSmith and Langfuse
- 6.1 Test sets: normal, edge, and adversarial cases; success in business terms
- 6.2 Tracing LangChain/LangGraph runs in LangSmith; datasets and experiments
- 6.3 The same traces and evals in Langfuse (open source, self-hostable); comparing the two
- 6.4 LLM-as-judge calibrated by human review; turning a failure into a regression test

**Deliverable:** an evaluation scorecard and a trace showing why a run succeeded or failed.

### Module 7: Deploy + recover with Temporal
- 7.1 Temporal workflows and activities; long waits for approvals
- 7.2 Recovery: check receipts before retrying a write
- 7.3 FastAPI service in Docker; secrets, access control, budgets, monitoring, rollback

**Deliverable:** a shareable pilot, an operating checklist, and a recovery demonstration.

### Module 8: Capstone: your domain pilot
Adapt DoubleAgent to a business task you know. Demo an approved action, a rejected action,
and a controlled failure with evaluation evidence; write the rollout proposal.

**Deliverable:** working pilot, short demo, realistic rollout proposal.

## Python concepts

Every lesson deliberately uses specific language features and standard-library modules.
See [PYTHON_CONCEPTS.md](PYTHON_CONCEPTS.md) for the full map.
