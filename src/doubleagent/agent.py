"""Your first agent: the tool-use loop, written by hand (Lesson 1.2).

chatbot  = one call
workflow = your code decides the steps
agent    = the model decides the next step (which tool, or stop), your code executes it, repeat
"""

import logging

from anthropic import AsyncAnthropic
from anthropic.types import MessageParam, ToolResultBlockParam
from pydantic import BaseModel

from doubleagent.erp import SupplierDirectory
from doubleagent.tools import TOOLS, ToolError, execute_tool

# One logger per module, named after it. (C#: ILogger<T>.) Configured once in cli.py.
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are DoubleAgent, a procurement assistant for Acme Industrial. "
    "Answer questions about suppliers using the lookup_supplier tool. "
    "Only state facts the tool returned; if a supplier isn't found, say so."
)


class AgentResult(BaseModel):
    answer: str
    tool_calls: list[str]
    turns: int


class MaxTurnsExceeded(Exception):
    """The model kept calling tools past the turn budget."""


async def run_agent(
    client: AsyncAnthropic,
    question: str,
    directory: SupplierDirectory,
    *,
    model: str,
    max_tokens: int,
    max_turns: int = 5,
) -> AgentResult:
    """Run the think -> act -> observe loop until the model stops asking for tools.

    `turns` is the number of model calls made. `tool_calls` lists tool names in call order.
    """
    # The conversation so far. Every turn resends all of it: the API is stateless.
    messages: list[MessageParam] = [{"role": "user", "content": question}]
    tool_calls: list[str] = []

    # `range(1, n + 1)` yields 1..n (C#: for (var turn = 1; turn <= n; turn++)).
    for turn in range(1, max_turns + 1):
        # THINK: the model decides whether to answer or to ask for tools.
        response = await client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )
        # Send back the WHOLE content (thinking + tool_use), not just the text:
        # the model needs its own earlier reasoning and tool calls to continue.
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            answer = "".join(b.text for b in response.content if b.type == "text")
            return AgentResult(answer=answer, tool_calls=tool_calls, turns=turn)

        # ACT: run every tool the model asked for (it may ask for several at once).
        results: list[ToolResultBlockParam] = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            tool_calls.append(block.name)
            # %-style args: formatted only if INFO is enabled (C#: ILogger message templates).
            logger.info("tool %s(%s)", block.name, block.input)
            try:
                result = execute_tool(block.name, block.input, directory)
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": result})
            except ToolError as error:
                # Errors are results, not crashes: the model sees them and can recover.
                results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(error),
                        "is_error": True,
                    }
                )

        # OBSERVE: all tool results go back in ONE user message.
        messages.append({"role": "user", "content": results})

    # Bound the loop so a confused model can't spend forever (C#: throw after N retries).
    raise MaxTurnsExceeded(f"no final answer after {max_turns} turns")
