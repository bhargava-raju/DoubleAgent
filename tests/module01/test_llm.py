from anthropic import Omit, omit

from doubleagent.llm import Answer, ask
from tests.fakes import FakeAnthropic, make_message, text, thinking


async def test_returns_text_and_usage() -> None:
    fake = FakeAnthropic([make_message(text("Paris"), input_tokens=12, output_tokens=3)])

    answer = await ask(fake.as_client(), "Capital of France?", model="m", max_tokens=100)

    assert answer == Answer(text="Paris", stop_reason="end_turn", input_tokens=12, output_tokens=3)


async def test_sends_question_model_and_max_tokens() -> None:
    fake = FakeAnthropic([make_message(text("ok"))])

    await ask(fake.as_client(), "Hello?", model="claude-haiku-4-5", max_tokens=256)

    call = fake.messages.calls[0]
    assert call["model"] == "claude-haiku-4-5"
    assert call["max_tokens"] == 256
    assert call["messages"] == [{"role": "user", "content": "Hello?"}]
    # No system prompt: either leave it out, or pass the SDK's `omit` sentinel.
    assert isinstance(call.get("system", omit), Omit)


async def test_passes_system_prompt_when_given() -> None:
    fake = FakeAnthropic([make_message(text("ok"))])

    await ask(fake.as_client(), "Hi", model="m", max_tokens=10, system="Be terse.")

    assert fake.messages.calls[0]["system"] == "Be terse."


async def test_skips_thinking_blocks_and_joins_text() -> None:
    fake = FakeAnthropic([make_message(thinking(), text("Hello, "), text("world"))])

    answer = await ask(fake.as_client(), "Hi", model="m", max_tokens=10)

    assert answer.text == "Hello, world"


async def test_reports_truncation() -> None:
    fake = FakeAnthropic([make_message(text("cut o"), stop_reason="max_tokens")])

    answer = await ask(fake.as_client(), "Write a novel", model="m", max_tokens=5)

    assert answer.stop_reason == "max_tokens"
