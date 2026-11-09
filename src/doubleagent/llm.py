"""A single, typed LLM call (Lesson 1.1).

This is a *chatbot* building block: one question in, one answer out. No tools, no loop.
"""

from anthropic import AsyncAnthropic, omit
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

    C# analogy: `Task<Answer> AskAsync(...)` wrapping one HTTP call and mapping the result
    to a record.
    """
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

    return Answer(
        text=text,
        stop_reason=response.stop_reason,
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens,
    )
