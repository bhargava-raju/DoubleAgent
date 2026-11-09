from functools import lru_cache
from typing import Literal, Self

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_MODEL = "claude-opus-5-5"
Provider = Literal["anthropic", "foundry"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    provider: Provider = "anthropic"

    anthropic_api_key: SecretStr | None = None
    anthropic_foundry_api_key: SecretStr | None = None
    anthropic_foundry_resource: str | None = None
    model: str = DEFAULT_MODEL

    max_tokens: int = Field(default=16000, gt=0)

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


@lru_cache
def get_settings() -> Settings:
    return Settings()
