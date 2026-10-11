"""Typed application settings (Lesson 1.1).

C# analogy: an options class bound from appsettings/env vars, validated at startup.
"""

from functools import lru_cache
from typing import Literal, Self  # noqa: F401  (you will need these)

from pydantic import Field, SecretStr, model_validator  # noqa: F401  (you will need these)
from pydantic_settings import BaseSettings, SettingsConfigDict  # noqa: F401

DEFAULT_MODEL = "claude-opus-5-5"

# Where Claude is called from:
#   "anthropic": Anthropic's API, authenticated with ANTHROPIC_API_KEY
#   "foundry":   your Microsoft Foundry (Azure) resource, with ANTHROPIC_FOUNDRY_API_KEY
#                and ANTHROPIC_FOUNDRY_RESOURCE
Provider = Literal["anthropic", "foundry"]


class Settings(BaseSettings):
    """Reads settings from the environment or a `.env` file (names are case-insensitive).

    TODO (1.1):
      - set `model_config` so values are also read from ".env" and unknown variables are ignored
        (look up `SettingsConfigDict(env_file=..., extra=...)`)
      - declare the fields:
          provider: Provider, defaulting to "anthropic"
          anthropic_api_key: SecretStr | None, default None
          anthropic_foundry_api_key: SecretStr | None, default None
          anthropic_foundry_resource: str | None, default None
              (the resource name, e.g. "my-resource" for https://my-resource.services.ai.azure.com)
          model: str, defaulting to DEFAULT_MODEL
          max_tokens: int, defaulting to 16000, must be > 0 (hint: `Field(gt=0)`)
      - add a validator that runs after field validation and checks the provider has
        its credentials:
          @model_validator(mode="after")
          def _check_credentials(self) -> Self: ...
        "anthropic" needs anthropic_api_key; "foundry" needs both foundry fields.
        Raise ValueError with a message naming the missing environment variable(s);
        Pydantic turns it into a ValidationError. (C#: IValidateOptions<T>.)
    """


@lru_cache
def get_settings() -> Settings:
    """Return one shared Settings instance (a lazy singleton).

    TODO (1.1): construct and return Settings(). `@lru_cache` makes later calls reuse it.
    """
    raise NotImplementedError
