"""Create the Claude client (Lesson 1.1).

C# analogy: a factory registered in DI that returns the client the app depends on.
For now the app targets Claude Sonnet through the Anthropic API only. Microsoft Foundry
support (`AsyncAnthropicFoundry`, a subclass of `AsyncAnthropic`) is deferred until the agent
works end to end; because the rest of the app only depends on `AsyncAnthropic`, adding it later
only touches this file.
"""

from anthropic import AsyncAnthropic

from doubleagent.config import Settings


def create_client(settings: Settings) -> AsyncAnthropic:
    """Return an async Anthropic client built from `settings`.

    TODO (1.1):
      - Return AsyncAnthropic(api_key=...).
      - Use `.get_secret_value()` to unwrap the SecretStr key.
      The caller owns the client and closes it with `async with create_client(s) as client:`.
    """
    raise NotImplementedError
