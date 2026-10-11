"""Typed application settings (Lesson 1.1).

C# analogy: an options class bound from appsettings/env vars, validated at startup.
"""

from functools import lru_cache
from typing import Literal, Self

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_MODEL = "claude-opus-5-5"

# Where Claude is called from:
#   "anthropic": Anthropic's API, authenticated with ANTHROPIC_API_KEY
#   "foundry":   your Microsoft Foundry (Azure) resource, with ANTHROPIC_FOUNDRY_API_KEY
#                and ANTHROPIC_FOUNDRY_RESOURCE
Provider = Literal["anthropic", "foundry"]


class Settings(BaseSettings):
    """Reads settings from the environment or a `.env` file (names are case-insensitive).

    Each field binds to the env var of the same name: `max_tokens` <- MAX_TOKENS.
    Real environment variables win over `.env`, like env vars over appsettings.json in .NET.
    """

    # Class-level config, ≈ `builder.Configuration.AddEnvironmentVariables()` plus a file source.
    # extra="ignore": other variables in .env (PATH, unrelated keys) are not errors.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # `name: type = default` declares a field. Literal allows only the listed strings (≈ an enum).
    provider: Provider = "anthropic"
    # SecretStr prints as '**********' in logs and reprs; call .get_secret_value() to read it.
    anthropic_api_key: SecretStr | None = None
    anthropic_foundry_api_key: SecretStr | None = None
    anthropic_foundry_resource: str | None = None
    model: str = DEFAULT_MODEL
    # Field(...) adds validation metadata, ≈ [Range(1, int.MaxValue)].
    max_tokens: int = Field(default=16000, gt=0)

    # Runs after every field is parsed, so it can check cross-field rules (≈ IValidateOptions<T>).
    # Returning `Self` (the instance) is required for mode="after".
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
        missing = [name for name, value in required.items() if not value]
        if missing:
            # Pydantic wraps this ValueError in a ValidationError that names the problem.
            raise ValueError(f"PROVIDER={self.provider} needs: {', '.join(missing)}")
        return self


@lru_cache
def get_settings() -> Settings:
    """Return one shared Settings instance (a lazy singleton).

    `@lru_cache` memoizes the call, so later calls reuse the first instance
    (≈ services.AddSingleton). Tests call `get_settings.cache_clear()` to reset it.
    """
    return Settings()
