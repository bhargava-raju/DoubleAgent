"""Typed application settings (Lesson 1.1).

C# analogy: an options class bound from appsettings/env vars, validated at startup.
"""

from functools import lru_cache

from pydantic import Field, SecretStr  # noqa: F401  (you will need these)
from pydantic_settings import BaseSettings, SettingsConfigDict  # noqa: F401

DEFAULT_MODEL = "claude-opus-5-5"


class Settings(BaseSettings):
    """Reads ANTHROPIC_API_KEY, MODEL, MAX_TOKENS from the environment or a `.env` file.

    TODO (1.1):
      - set `model_config` so values are also read from ".env" and unknown variables are ignored
        (look up `SettingsConfigDict(env_file=..., extra=...)`)
      - declare the fields:
          anthropic_api_key: a required secret string (SecretStr)
          model: str, defaulting to DEFAULT_MODEL
          max_tokens: int, defaulting to 16000, must be > 0 (hint: `Field(gt=0)`)
    """


@lru_cache
def get_settings() -> Settings:
    """Return one shared Settings instance (a lazy singleton).

    TODO (1.1): construct and return Settings(). `@lru_cache` makes later calls reuse it.
    """
    raise NotImplementedError
