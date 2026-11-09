"""Typed application settings (Lesson 1.1).

C# analogy: an options class bound from appsettings/env vars, validated at startup.
"""

import logging
from functools import lru_cache
from typing import Literal, Self

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "claude-sonnet-5-5"
# Literal allows only the listed strings (≈ an enum).
Provider = Literal["anthropic", "foundry"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]


class Settings(BaseSettings):
    """Reads fields from env vars or `.env` (`max_tokens` <- MAX_TOKENS)."""

    """ Real env vars win over `.env`."""

    # extra="ignore": unrelated variables in .env are not errors.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    provider: Provider = "anthropic"

    # SecretStr prints as '**********' in logs; call .get_secret_value() to read it.
    anthropic_api_key: SecretStr | None = None
    anthropic_foundry_api_key: SecretStr | None = None
    anthropic_foundry_resource: str | None = None
    model: str = DEFAULT_MODEL

    # Field(...) adds validation, ≈ [Range(1, int.MaxValue)].
    max_tokens: int = Field(default=16000, gt=0)

    # LOG_LEVEL in .env. DEBUG also shows the SDK's own HTTP logs.
    log_level: LogLevel = "INFO"

    # Runs after all fields are parsed, so it can check cross-field rules (≈ IValidateOptions<T>).
    @model_validator(mode="after")
    def _check_credentials(self) -> Self:
        required: dict[str, object] = (
            {"ANTHROPIC_API_KEY": self.anthropic_api_key}
            if self.provider == "anthropic"
            else {
                "ANTHROPIC_FOUNDRY_API_KEY": self.anthropic_foundry_api_key,
                "ANTHROPIC_FOUNDRY_RESOURCE": self.anthropic_foundry_resource,
            }
        )
        # A list comprehension: ≈ required.Where(kv => kv.Value is null).Select(kv => kv.Key).
        missing: list[str] = [name for name, value in required.items() if not value]
        if missing:
            # Pydantic wraps this ValueError in a ValidationError that names the problem.
            raise ValueError(f"PROVIDER={self.provider} needs: {', '.join(missing)}")
        return self


# @lru_cache memoizes the call: one shared instance (≈ services.AddSingleton).
# Tests reset it with get_settings.cache_clear().
@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    # Log what was loaded, never the secret itself (only whether it is set).
    logger.info(
        "settings loaded: provider=%s model=%s max_tokens=%d api_key_set=%s",
        settings.provider,
        settings.model,
        settings.max_tokens,
        settings.anthropic_api_key is not None,
    )
    return settings
