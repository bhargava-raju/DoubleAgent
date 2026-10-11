"""Create the Claude client for the configured provider (Lesson 1.1).

C# analogy: a factory registered in DI that returns the right implementation for the environment.
`AsyncAnthropicFoundry` is a subclass of `AsyncAnthropic`, so the rest of the app only ever
depends on `AsyncAnthropic` and never needs to know which provider is behind it.
"""

from anthropic import AsyncAnthropic, AsyncAnthropicFoundry  # noqa: F401  (you will need these)

from doubleagent.config import Settings


def create_client(settings: Settings) -> AsyncAnthropic:
    """Return an async client for `settings.provider`.

    TODO (1.1):
      - "anthropic": AsyncAnthropic(api_key=...)
      - "foundry":   AsyncAnthropicFoundry(api_key=..., resource=...)
      Use `.get_secret_value()` to unwrap the SecretStr keys. A `match` statement fits well here.
      The caller owns the client and closes it with `async with create_client(s) as client:`.
    """
    raise NotImplementedError
