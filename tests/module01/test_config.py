import pytest
from pydantic import ValidationError

from doubleagent.config import DEFAULT_MODEL, Settings, get_settings


@pytest.fixture(autouse=True)
def isolated_env(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    # Run from an empty folder so your real .env is not picked up, and clear related env vars.
    monkeypatch.chdir(tmp_path)
    for name in ("ANTHROPIC_API_KEY", "MODEL", "MAX_TOKENS"):
        monkeypatch.delenv(name, raising=False)
    get_settings.cache_clear()


def test_reads_api_key_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-123")
    settings = Settings()  # pyright: ignore[reportCallIssue]
    assert settings.anthropic_api_key.get_secret_value() == "sk-test-123"


def test_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    settings = Settings()  # pyright: ignore[reportCallIssue]
    assert settings.model == DEFAULT_MODEL
    assert settings.max_tokens == 16000


def test_api_key_is_hidden_when_printed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-secret")
    assert "sk-secret" not in repr(Settings())  # pyright: ignore[reportCallIssue]


def test_missing_api_key_fails_fast() -> None:
    with pytest.raises(ValidationError):
        Settings()  # pyright: ignore[reportCallIssue]


def test_max_tokens_must_be_positive(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    monkeypatch.setenv("MAX_TOKENS", "0")
    with pytest.raises(ValidationError):
        Settings()  # pyright: ignore[reportCallIssue]


def test_reads_dotenv_file(tmp_path) -> None:
    (tmp_path / ".env").write_text("ANTHROPIC_API_KEY=sk-from-file\nSOMETHING_ELSE=1\n")
    assert Settings().anthropic_api_key.get_secret_value() == "sk-from-file"  # pyright: ignore[reportCallIssue]


def test_get_settings_is_cached(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    assert get_settings() is get_settings()
