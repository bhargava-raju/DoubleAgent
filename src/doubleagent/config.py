"""Typed application settings (Lesson 1.1).

C# analogy: an options class bound from appsettings/env vars, validated at startup.

Do the steps in order. After each one, run only that step's tests, e.g.
    uv run pytest tests/module01/test_config.py -q -k defaults
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

    Each field binds to the env var of the same name: `max_tokens` <- MAX_TOKENS.

    TODO step 1 (plain fields). Tests: -k "defaults or unknown_provider"
      Declare fields with `name: type = default`:
          provider: Provider, defaulting to "anthropic"
          model: str, defaulting to DEFAULT_MODEL
          max_tokens: int, defaulting to 16000

    TODO step 2 (secrets). Tests: -k "reads_api_key or hidden"
      Add the credential fields. SecretStr hides the value when printed (≈ not logging a secret).
          anthropic_api_key: SecretStr | None, default None
          anthropic_foundry_api_key: SecretStr | None, default None
          anthropic_foundry_resource: str | None, default None
              (the resource name, e.g. "my-resource" for https://my-resource.services.ai.azure.com)

    TODO step 3 (.env file). Tests: -k dotenv
      Set the class attribute `model_config = SettingsConfigDict(env_file=..., extra=...)`
      so values are also read from ".env" and unknown variables in it are ignored.

    TODO step 4 (range check). Tests: -k max_tokens
      Make max_tokens reject 0 and negatives: `Field(default=..., gt=0)`
      (≈ [Range(1, int.MaxValue)]).

    TODO step 5 (cross-field check). Tests: -k "missing or foundry_settings or foundry_requires"
      Add a validator that runs after all fields are parsed (≈ IValidateOptions<T>):
          @model_validator(mode="after")
          def _check_credentials(self) -> Self: ...
      "anthropic" needs anthropic_api_key; "foundry" needs both foundry fields.
      Raise ValueError with a message naming the missing environment variable(s),
      then `return self`. Pydantic turns the ValueError into a ValidationError.
    """


@lru_cache
def get_settings() -> Settings:
    """Return one shared Settings instance (a lazy singleton).

    TODO step 6. Tests: -k cached
      Construct and return Settings(). `@lru_cache` makes later calls reuse it
      (≈ services.AddSingleton).
    """
    raise NotImplementedError
