"""Test doubles for the Anthropic client. Provided for you; read it, don't edit it.

Python needs no IAnthropicClient interface: any object with a `.messages.create` coroutine
works ("duck typing"). `as_client()` casts the fake so pyright accepts it where an
AsyncAnthropic is expected.
"""

import copy
from typing import Any, cast

from anthropic import AsyncAnthropic
from anthropic.types import Message


def make_message(
    *blocks: dict[str, Any],
    stop_reason: str = "end_turn",
    input_tokens: int = 100,
    output_tokens: int = 20,
    model: str = "claude-opus-5-5",
) -> Message:
    """Build a real `anthropic.types.Message`, exactly as the SDK would return it."""
    return Message.model_validate(
        {
            "id": "msg_test",
            "type": "message",
            "role": "assistant",
            "model": model,
            "content": list(blocks),
            "stop_reason": stop_reason,
            "stop_sequence": None,
            "usage": {"input_tokens": input_tokens, "output_tokens": output_tokens},
        }
    )


def text(value: str) -> dict[str, Any]:
    return {"type": "text", "text": value}


def thinking() -> dict[str, Any]:
    return {"type": "thinking", "thinking": "", "signature": "sig"}


def tool_use(name: str, tool_input: dict[str, Any], tool_id: str = "toolu_1") -> dict[str, Any]:
    return {"type": "tool_use", "id": tool_id, "name": name, "input": tool_input}


class FakeMessages:
    def __init__(self, responses: list[Message] | None = None) -> None:
        self._responses = list(responses or [])
        self.calls: list[dict[str, Any]] = []

    async def create(self, **kwargs: Any) -> Message:
        # Deep copy: the code under test may keep mutating its `messages` list after the call.
        self.calls.append(copy.deepcopy(kwargs))
        if not self._responses:
            raise AssertionError("FakeMessages ran out of scripted responses")
        response = self._responses.pop(0)
        if kwargs.get("model") and response.model != kwargs["model"]:
            response = response.model_copy(update={"model": kwargs["model"]})
        return response


class FakeAnthropic:
    def __init__(self, responses: list[Message] | None = None) -> None:
        self.messages = FakeMessages(responses)

    def as_client(self) -> AsyncAnthropic:
        return cast(AsyncAnthropic, self)
