"""Command-line entry point: `uv run doubleagent <command> ...` (Lessons 1.1 - 1.3).

C# analogy: `static async Task Main(string[] args)` plus System.CommandLine.
"""

import argparse
import asyncio
import logging

from doubleagent.client import create_client
from doubleagent.config import get_settings
from doubleagent.llm import ask
from doubleagent.logging_setup import configure_logging

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="doubleagent")
    sub = parser.add_subparsers(dest="command", required=True)

    ask_cmd = sub.add_parser("ask", help="one question, one answer (a chatbot)")
    ask_cmd.add_argument("question")

    agent_cmd = sub.add_parser("agent", help="ask the supplier agent (uses tools)")
    agent_cmd.add_argument("question")

    sub.add_parser("compare", help="run the model comparison scorecard")
    return parser


async def _run(args: argparse.Namespace) -> None:
    """The async part of the program (C#: the body of `async Task Main`)."""
    settings = get_settings()
    # `async with` disposes the client when the block ends (C#: `await using`).
    async with create_client(settings) as client:
        # `match` is Python's switch statement; `case _` is `default`.
        match args.command:
            case "ask":
                answer = await ask(
                    client, args.question, model=settings.model, max_tokens=settings.max_tokens
                )
                print(answer.text)
                # First telemetry: tokens in/out and why the model stopped.
                print(
                    f"\n[{answer.input_tokens} in / {answer.output_tokens} out tokens, "
                    f"stop_reason={answer.stop_reason}]"
                )
                if answer.stop_reason == "max_tokens":
                    print("Warning: the answer was cut off; raise MAX_TOKENS.")
            case _:
                # TODO (1.2): "agent" -> agent.run_agent; (1.3): "compare" -> scorecard.
                raise NotImplementedError(f"command {args.command!r} is not implemented yet")


def main() -> None:
    """Parse args, then bridge from sync to async with asyncio.run
    (C#: `Main` calling `RunAsync().GetAwaiter().GetResult()`).
    """
    args = build_parser().parse_args()
    configure_logging()  # INFO until settings tell us the real level
    configure_logging(get_settings().log_level)  # cached, so _run reuses the same Settings
    logger.info("command %r started", args.command)
    asyncio.run(_run(args))


if __name__ == "__main__":  # lets `python -m doubleagent.cli` (and the VS Code debugger) run it
    main()
