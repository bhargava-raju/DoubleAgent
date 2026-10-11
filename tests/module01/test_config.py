import pytest
from anthropic import AsyncAnthropic, AsyncAnthropicFoundry
from pydantic import ValidationError

from doubleagent.client import create_client
from doubleagent.config import DEFAULT_MODEL, Settings, get_settings

ENV_VARS = (
    "PROVIDER",
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_FOUNDRY_API_KEY",
    "ANTHROPIC_FOUNDRY_RESOURCE",
    "MODEL",
    "MAX_TOKENS",
)


@pytest.fixture(autouse=True)
def isolated_env(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    # Run from an empty folder so your real .env is not picked up, and clear related env vars.
    monkeypatch.chdir(tmp_path)
    for name in ENV_VARS:
        monkeypatch.delenv(name, raising=False)
    get_settings.cache_clear()


def test_reads_api_key_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-123")
    settings = Settings()
    assert settings.provider == "anthropic"
    assert settings.anthropic_api_key is not None
    assert settings.anthropic_api_key.get_secret_value() == "sk-test-123"


def test_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    settings = Settings()
    assert settings.model == DEFAULT_MODEL
    assert settings.max_tokens == 16000


def test_api_key_is_hidden_when_printed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-secret")
    assert "sk-secret" not in repr(Settings())


def test_missing_api_key_fails_fast() -> None:
    with pytest.raises(ValidationError, match="ANTHROPIC_API_KEY"):
        Settings()


def test_max_tokens_must_be_positive(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    monkeypatch.setenv("MAX_TOKENS", "0")
    with pytest.raises(ValidationError):
        Settings()


def test_reads_dotenv_file(tmp_path) -> None:
    (tmp_path / ".env").write_text("ANTHROPIC_API_KEY=sk-from-file\nSOMETHING_ELSE=1\n")
    key = Settings().anthropic_api_key
    assert key is not None and key.get_secret_value() == "sk-from-file"


def test_get_settings_is_cached(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    assert get_settings() is get_settings()


def test_foundry_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PROVIDER", "foundry")
    monkeypatch.setenv("ANTHROPIC_FOUNDRY_API_KEY", "az-key")
    monkeypatch.setenv("ANTHROPIC_FOUNDRY_RESOURCE", "acme-ai")
    settings = Settings()
    assert settings.provider == "foundry"
    assert settings.anthropic_foundry_resource == "acme-ai"
    assert settings.anthropic_api_key is None  # not needed for Foundry


@pytest.mark.parametrize(
    ("env", "missing"),
    [
        ({"ANTHROPIC_FOUNDRY_RESOURCE": "acme-ai"}, "ANTHROPIC_FOUNDRY_API_KEY"),
        ({"ANTHROPIC_FOUNDRY_API_KEY": "az-key"}, "ANTHROPIC_FOUNDRY_RESOURCE"),
    ],
)
def test_foundry_requires_key_and_resource(
    monkeypatch: pytest.MonkeyPatch, env: dict[str, str], missing: str
) -> None:
    monkeypatch.setenv("PROVIDER", "foundry")
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    with pytest.raises(ValidationError, match=missing):
        Settings()


def test_unknown_provider_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PROVIDER", "openai")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    with pytest.raises(ValidationError):
        Settings()


async def test_create_client_anthropic(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    async with create_client(Settings()) as client:
        assert type(client) is AsyncAnthropic
        assert client.api_key == "sk-test"


async def test_create_client_foundry(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PROVIDER", "foundry")
    monkeypatch.setenv("ANTHROPIC_FOUNDRY_API_KEY", "az-key")
    monkeypatch.setenv("ANTHROPIC_FOUNDRY_RESOURCE", "acme-ai")
    async with create_client(Settings()) as client:
        assert isinstance(client, AsyncAnthropicFoundry)
        assert "acme-ai.services.ai.azure.com" in str(client.base_url)
