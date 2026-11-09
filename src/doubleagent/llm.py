"""A single, typed LLM call (Lesson 1.1).

This is a *chatbot* building block: one question in, one answer out. No tools, no loop.
"""

import logging
import time

from anthropic import AsyncAnthropic, omit
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class Answer(BaseModel):
    """What we keep from one Messages API response. (C#: a record DTO.)"""

    text: str
    stop_reason: str | None
    input_tokens: int
    output_tokens: int


async def ask(
    client: AsyncAnthropic,
    question: str,
    *,
    model: str,
    max_tokens: int,
    system: str | None = None,
) -> Answer:
    """Send one user question to Claude and return the answer text plus usage.

    C# analogy: `Task<Answer> AskAsync(...)` wrapping one HTTP call and mapping the result
    to a record.
    """
    logger.debug("ask: model=%s max_tokens=%d question_chars=%d", model, max_tokens, len(question))
    # perf_counter() is a monotonic high-resolution clock (C#: Stopwatch).
    started = time.perf_counter()
    response = await client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": question}],
        # `omit` leaves the parameter out entirely; `None` would be sent as JSON null.
        # `a if cond else b` is Python's ternary (C#: `cond ? a : b`).
        system=system if system is not None else omit,
    )

    # `content` is a list of blocks (text, thinking, tool_use...). Keep only text.
    # A generator expression inside join. C#:
    # `string.Join("", content.OfType<TextBlock>().Select(b => b.Text))`.
    text = "".join(block.text for block in response.content if block.type == "text")

    elapsed_ms = (time.perf_counter() - started) * 1000
    logger.info(
        "llm call: model=%s %.0f ms, %d in / %d out tokens, stop_reason=%s",
        model,
        elapsed_ms,
        response.usage.input_tokens,
        response.usage.output_tokens,
        response.stop_reason,
    )
    if response.stop_reason == "max_tokens":
        logger.warning("answer truncated at max_tokens=%d", max_tokens)

    return Answer(
        text=text,
        stop_reason=response.stop_reason,
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens,
    )
