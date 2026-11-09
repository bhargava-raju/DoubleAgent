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

    The caller owns the client and closes it with `async with create_client(s) as client:`
    (C#: `await using var client = ...`).
    """
    key = settings.anthropic_api_key
    # The type is `SecretStr | None`, so narrow it before use (C#: a null check on a nullable).
    # Settings already validated this; the check keeps pyright and future refactors honest.
    if key is None:
        raise ValueError("ANTHROPIC_API_KEY is not set")
    # SecretStr hides the value in logs; unwrap it only where the SDK needs the real string.
    return AsyncAnthropic(api_key=key.get_secret_value())
