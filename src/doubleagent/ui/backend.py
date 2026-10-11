"""The UI's only door into the app (Lesson 1.5).

Keeping Streamlit code out of here means the UI stays thin and this layer stays testable.
C# analogy: an application-service layer that controllers/Blazor components call.
"""

from collections.abc import Sequence

from pydantic import ValidationError  # noqa: F401  (you will need these)

from doubleagent.agent import AgentResult, run_agent  # noqa: F401
from doubleagent.client import create_client  # noqa: F401
from doubleagent.config import get_settings  # noqa: F401
from doubleagent.erp import SupplierDirectory  # noqa: F401
from doubleagent.scorecard import ScorecardRow, compare_models  # noqa: F401


def config_error() -> str | None:
    """Return a friendly message if settings can't load (e.g. no API key), else None.

    TODO (1.5):
      - clear the settings cache first (`get_settings.cache_clear()`) so a new .env is picked up
      - try get_settings(); on ValidationError return a message that names the missing setting
        (e.g. ANTHROPIC_API_KEY) and tells the user how to fix it. Never include a key itself.
    """
    raise NotImplementedError


async def answer(question: str, *, model: str, max_turns: int) -> AgentResult:
    """TODO (1.5): load settings, open a client with
    `async with create_client(settings) as client:`,
    and return the result of run_agent(...) over the supplier directory."""
    raise NotImplementedError


async def compare(
    task: str, models: Sequence[str], expected_keywords: Sequence[str]
) -> list[ScorecardRow]:
    """TODO (1.5): like `answer`, but call compare_models(...)."""
    raise NotImplementedError
