"""A single, typed LLM call (Lesson 1.1).

This is a *chatbot* building block: one question in, one answer out. No tools, no loop.
"""

from anthropic import AsyncAnthropic, omit  # noqa: F401  (see the TODO)
from pydantic import BaseModel


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

    TODO (1.1):
      - await `client.messages.create(...)` with model, max_tokens and one user message
      - `system` is optional: pass `system=system if system is not None else omit`
        (`omit` is the SDK's "leave this parameter out" sentinel; `None` would be sent as null)
      - the response's `content` is a list of blocks; keep only blocks whose `.type == "text"`
        and join their `.text` (thinking blocks may appear before the text: skip them)
      - fill and return an `Answer` from the text, `stop_reason` and `usage`
    """
    raise NotImplementedError
