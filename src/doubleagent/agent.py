"""Your first agent: the tool-use loop, written by hand (Lesson 1.2).

chatbot  = one call
workflow = your code decides the steps
agent    = the model decides the next step (which tool, or stop), your code executes it, repeat
"""

import logging

from anthropic import AsyncAnthropic
from anthropic.types import MessageParam  # noqa: F401  (type for your messages list)
from pydantic import BaseModel

from doubleagent.erp import SupplierDirectory
from doubleagent.tools import TOOLS, ToolError, execute_tool  # noqa: F401

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

    TODO (1.2):
      1. messages: list[MessageParam] starts with the user's question
      2. loop at most `max_turns` times:
           response = await client.messages.create(model, max_tokens, system=SYSTEM_PROMPT,
                                                   tools=TOOLS, messages=messages)
           append {"role": "assistant", "content": response.content}   <- the WHOLE content list,
               including thinking and tool_use blocks, not just the text
           if response.stop_reason != "tool_use": return an AgentResult with the joined text
           otherwise, for EVERY tool_use block in response.content:
               run execute_tool(...) and build a tool_result block:
                 {"type": "tool_result", "tool_use_id": block.id, "content": result}
               if it raised ToolError, still send a tool_result with the error message
                 and "is_error": True
           append ONE user message holding all the tool_result blocks
      3. if the loop runs out, raise MaxTurnsExceeded

    `turns` is the number of model calls made. `tool_calls` lists tool names in call order.
    Log each tool call with logger.info(...) using %-style args, e.g.
    logger.info("tool %s(%s)", block.name, block.input)  <- lazy formatting, like ILogger templates
    """
    raise NotImplementedError
