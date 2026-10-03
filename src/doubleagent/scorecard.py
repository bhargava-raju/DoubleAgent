"""Model comparison scorecard (Lesson 1.3): quality, latency and cost on one task."""

import asyncio  # noqa: F401  (bonus: asyncio.gather)
import csv  # noqa: F401  (you will need it)
import time  # noqa: F401  (you will need it)
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from anthropic import AsyncAnthropic
from pydantic import BaseModel

from doubleagent.llm import ask  # noqa: F401  (you will need it)


@dataclass(frozen=True, slots=True)
class Pricing:
    """USD per million tokens. A frozen dataclass: an immutable value object (C#: a record).

    Unlike Pydantic models, dataclasses do no validation; use them for internal values
    you construct yourself, and Pydantic at boundaries (config, API input/output, LLM output).
    """

    input_per_mtok: float
    output_per_mtok: float


# Check https://www.anthropic.com/pricing before relying on these.
PRICES: dict[str, Pricing] = {
    "claude-haiku-4-5": Pricing(1.00, 5.00),
    "claude-sonnet-5-5": Pricing(2.00, 10.00),
    "claude-opus-5-5": Pricing(4.00, 20.00),
}


class ScorecardRow(BaseModel):
    model: str
    latency_ms: float
    input_tokens: int
    output_tokens: int
    cost_usd: float
    quality: float  # 0.0 - 1.0
    answer: str


def estimate_cost_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    """TODO (1.3): price the call using PRICES. Raise KeyError for an unknown model."""
    raise NotImplementedError


def keyword_quality(answer: str, expected_keywords: Sequence[str]) -> float:
    """TODO (1.3): fraction of expected keywords found in the answer, case-insensitive.

    Return 1.0 when there are no expected keywords. (A crude check; Module 6 replaces it
    with proper evals and an LLM judge.)
    """
    raise NotImplementedError


async def compare_models(
    client: AsyncAnthropic,
    task: str,
    models: Sequence[str],
    expected_keywords: Sequence[str],
    *,
    max_tokens: int = 16000,
) -> list[ScorecardRow]:
    """TODO (1.3): call `ask` once per model and build one ScorecardRow each.

    Measure latency with time.perf_counter() around the call.
    Bonus: run the models concurrently with asyncio.gather and keep the input order.
    """
    raise NotImplementedError


def render_markdown(rows: Sequence[ScorecardRow]) -> str:
    """TODO (1.3): render a Markdown table with columns, in this order:

    | Model | Quality | Latency (ms) | Input tokens | Output tokens | Cost (USD) |

    Quality as a percentage with no decimals (e.g. "67%"), latency with no decimals,
    cost with 6 decimals. One row per ScorecardRow, in the given order.
    """
    raise NotImplementedError


def write_csv(rows: Sequence[ScorecardRow], path: Path) -> None:
    """TODO (1.3): write the rows to a CSV file with a header row of the ScorecardRow field names.

    Hints: `csv.DictWriter`, `ScorecardRow.model_fields`, `row.model_dump()`,
    and open the file with `path.open("w", newline="", encoding="utf-8")` inside a `with` block.
    Create the parent folder if it doesn't exist (`path.parent.mkdir(...)`).
    """
    raise NotImplementedError
