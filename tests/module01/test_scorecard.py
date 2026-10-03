import csv
from pathlib import Path

import pytest

from doubleagent.scorecard import (
    ScorecardRow,
    compare_models,
    estimate_cost_usd,
    keyword_quality,
    render_markdown,
    write_csv,
)
from tests.fakes import FakeAnthropic, make_message, text


def test_estimate_cost() -> None:
    # Opus 5.5: $4 / MTok in, $20 / MTok out
    assert estimate_cost_usd("claude-opus-5-5", 1_000_000, 0) == pytest.approx(4.0)
    assert estimate_cost_usd("claude-opus-5-5", 2_000, 500) == pytest.approx(0.018)


def test_estimate_cost_unknown_model() -> None:
    with pytest.raises(KeyError):
        estimate_cost_usd("gpt-who", 1, 1)


def test_keyword_quality() -> None:
    score = keyword_quality("Initech is ON HOLD", ["initech", "on hold", "SUP-002"])
    assert score == pytest.approx(2 / 3)
    assert keyword_quality("anything", []) == 1.0


async def test_compare_models_builds_one_row_per_model_in_order() -> None:
    fake = FakeAnthropic(
        [
            make_message(text("Initech is on hold"), input_tokens=1000, output_tokens=100),
            make_message(text("No idea"), input_tokens=1000, output_tokens=10),
        ]
    )

    rows = await compare_models(
        fake.as_client(),
        "Is Initech approved?",
        ["claude-haiku-4-5", "claude-opus-5-5"],
        ["initech", "on hold"],
        max_tokens=100,
    )

    assert {r.model for r in rows} == {"claude-haiku-4-5", "claude-opus-5-5"}
    assert [r.model for r in rows] == ["claude-haiku-4-5", "claude-opus-5-5"]
    assert all(r.latency_ms >= 0 for r in rows)
    by_model = {r.model: r for r in rows}
    assert sorted(r.quality for r in rows) == [0.0, 1.0]
    for row in by_model.values():
        assert row.cost_usd == pytest.approx(
            estimate_cost_usd(row.model, row.input_tokens, row.output_tokens)
        )


def _row() -> ScorecardRow:
    return ScorecardRow(
        model="claude-haiku-4-5",
        latency_ms=812.4,
        input_tokens=1000,
        output_tokens=100,
        cost_usd=0.0015,
        quality=2 / 3,
        answer="...",
    )


def test_render_markdown() -> None:
    rows = [_row()]
    lines = render_markdown(rows).strip().splitlines()
    assert lines[0].replace(" ", "") == (
        "|Model|Quality|Latency(ms)|Inputtokens|Outputtokens|Cost(USD)|"
    )
    assert set(lines[1].replace("|", "").replace(" ", "")) <= {"-", ":"}
    cells = [c.strip() for c in lines[2].strip("|").split("|")]
    assert cells == ["claude-haiku-4-5", "67%", "812", "1000", "100", "0.001500"]


def test_write_csv(tmp_path: Path) -> None:
    target = tmp_path / "reports" / "scorecard.csv"

    write_csv([_row(), _row()], target)

    with target.open(newline="", encoding="utf-8") as f:
        records = list(csv.DictReader(f))
    assert len(records) == 2
    assert records[0]["model"] == "claude-haiku-4-5"
    assert float(records[0]["cost_usd"]) == pytest.approx(0.0015)
