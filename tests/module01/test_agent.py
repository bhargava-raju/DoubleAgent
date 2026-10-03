import json

import pytest

from doubleagent.agent import SYSTEM_PROMPT, AgentResult, MaxTurnsExceeded, run_agent
from doubleagent.erp import SupplierDirectory
from doubleagent.tools import LOOKUP_SUPPLIER, TOOLS
from tests.fakes import FakeAnthropic, make_message, text, thinking, tool_use


@pytest.fixture
def directory() -> SupplierDirectory:
    return SupplierDirectory.from_json_file()


async def test_answers_directly_without_tools(directory: SupplierDirectory) -> None:
    fake = FakeAnthropic([make_message(text("Hello! Ask me about suppliers."))])

    result = await run_agent(fake.as_client(), "hi", directory, model="m", max_tokens=100)

    assert result == AgentResult(answer="Hello! Ask me about suppliers.", tool_calls=[], turns=1)
    call = fake.messages.calls[0]
    assert call["system"] == SYSTEM_PROMPT
    assert call["tools"] == TOOLS


async def test_runs_tool_then_answers(directory: SupplierDirectory) -> None:
    first = make_message(
        thinking(),
        tool_use(LOOKUP_SUPPLIER, {"query": "Initech"}, tool_id="toolu_A"),
        stop_reason="tool_use",
    )
    fake = FakeAnthropic([first, make_message(text("Initech is on hold."))])

    result = await run_agent(
        fake.as_client(), "Can we order from Initech?", directory, model="m", max_tokens=100
    )

    assert result.answer == "Initech is on hold."
    assert result.tool_calls == [LOOKUP_SUPPLIER]
    assert result.turns == 2

    sent = fake.messages.calls[1]["messages"]
    assert [m["role"] for m in sent] == ["user", "assistant", "user"]
    # The whole assistant content (thinking + tool_use) goes back, unchanged.
    assert sent[1]["content"] == first.content
    (tool_result,) = sent[2]["content"]
    assert tool_result["type"] == "tool_result"
    assert tool_result["tool_use_id"] == "toolu_A"
    assert json.loads(tool_result["content"])["matches"][0]["id"] == "SUP-002"
    assert not tool_result.get("is_error", False)


async def test_parallel_tool_calls_go_back_in_one_message(directory: SupplierDirectory) -> None:
    first = make_message(
        tool_use(LOOKUP_SUPPLIER, {"query": "Globex"}, tool_id="toolu_1"),
        tool_use(LOOKUP_SUPPLIER, {"query": "Stark"}, tool_id="toolu_2"),
        stop_reason="tool_use",
    )
    fake = FakeAnthropic([first, make_message(text("done"))])

    result = await run_agent(fake.as_client(), "compare", directory, model="m", max_tokens=100)

    assert result.tool_calls == [LOOKUP_SUPPLIER, LOOKUP_SUPPLIER]
    results = fake.messages.calls[1]["messages"][2]["content"]
    assert [r["tool_use_id"] for r in results] == ["toolu_1", "toolu_2"]


async def test_tool_errors_are_reported_to_the_model(directory: SupplierDirectory) -> None:
    first = make_message(tool_use("drop_tables", {}, tool_id="toolu_X"), stop_reason="tool_use")
    fake = FakeAnthropic([first, make_message(text("I can't do that."))])

    result = await run_agent(fake.as_client(), "oops", directory, model="m", max_tokens=100)

    assert result.answer == "I can't do that."
    (tool_result,) = fake.messages.calls[1]["messages"][2]["content"]
    assert tool_result["tool_use_id"] == "toolu_X"
    assert tool_result["is_error"] is True


async def test_stops_after_max_turns(directory: SupplierDirectory) -> None:
    looping = [
        make_message(tool_use(LOOKUP_SUPPLIER, {"query": "x"}), stop_reason="tool_use")
        for _ in range(3)
    ]
    fake = FakeAnthropic(looping)

    with pytest.raises(MaxTurnsExceeded):
        await run_agent(fake.as_client(), "loop", directory, model="m", max_tokens=10, max_turns=3)
