from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from doubleagent.agent import AgentResult
from doubleagent.scorecard import ScorecardRow
from doubleagent.ui import backend

APP = str(Path(__file__).resolve().parents[2] / "src" / "doubleagent" / "ui" / "app.py")


@pytest.fixture
def configured(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(backend, "config_error", lambda: None)


def test_shows_error_without_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(backend, "config_error", lambda: "ANTHROPIC_API_KEY is not set")
    at = AppTest.from_file(APP).run()
    assert not at.exception
    assert "ANTHROPIC_API_KEY" in at.error[0].value
    assert len(at.chat_input) == 0


def test_chat_round_trip(configured: None, monkeypatch: pytest.MonkeyPatch) -> None:
    seen: dict[str, object] = {}

    async def fake_answer(question: str, *, model: str, max_turns: int) -> AgentResult:
        seen.update(question=question, model=model, max_turns=max_turns)
        return AgentResult(answer="Initech is on hold.", tool_calls=["lookup_supplier"], turns=2)

    monkeypatch.setattr(backend, "answer", fake_answer)
    at = AppTest.from_file(APP).run()
    at.chat_input[0].set_value("Is Initech approved?").run()

    assert not at.exception
    assert seen["question"] == "Is Initech approved?"
    texts = [m.markdown[0].value for m in at.chat_message]
    assert texts == ["Is Initech approved?", "Initech is on hold."]
    assert "lookup_supplier" in [c.value for c in at.code]


def test_scorecard_tab(configured: None, monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_compare(task, models, keywords) -> list[ScorecardRow]:
        return [
            ScorecardRow(
                model=m,
                latency_ms=1,
                input_tokens=1,
                output_tokens=1,
                cost_usd=0.1,
                quality=1,
                answer="x",
            )
            for m in models
        ]

    monkeypatch.setattr(backend, "compare", fake_compare)
    at = AppTest.from_file(APP).run()
    at.button(key="run_comparison").click().run()
    assert not at.exception
    assert len(at.dataframe) == 1


def test_history_survives_reruns_and_can_be_cleared(
    configured: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def echo(question: str, *, model: str, max_turns: int) -> AgentResult:
        return AgentResult(answer=f"echo: {question}", tool_calls=[], turns=1)

    monkeypatch.setattr(backend, "answer", echo)
    at = AppTest.from_file(APP).run()
    at.chat_input[0].set_value("one").run()
    at.chat_input[0].set_value("two").run()
    assert len(at.chat_message) == 4

    at.button(key="new_conversation").click().run()
    assert len(at.chat_message) == 0


def test_config_error_reports_missing_key(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    message = backend.config_error()
    assert message is not None and "ANTHROPIC_API_KEY" in message

    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    assert backend.config_error() is None
