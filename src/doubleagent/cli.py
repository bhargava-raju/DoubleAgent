"""Command-line entry point: `uv run doubleagent <command> ...` (Lessons 1.1 - 1.3).

C# analogy: `static async Task Main(string[] args)` plus System.CommandLine.
"""

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="doubleagent")
    sub = parser.add_subparsers(dest="command", required=True)

    ask_cmd = sub.add_parser("ask", help="one question, one answer (a chatbot)")
    ask_cmd.add_argument("question")

    agent_cmd = sub.add_parser("agent", help="ask the supplier agent (uses tools)")
    agent_cmd.add_argument("question")

    sub.add_parser("compare", help="run the model comparison scorecard")
    return parser


def main() -> None:
    """TODO: parse args, load settings, open `async with AsyncAnthropic(...) as client`,
    and dispatch on args.command with a `match` statement (C#: switch expression) to
    llm.ask (1.1), agent.run_agent (1.2) or scorecard.compare_models (1.3).

    Also: call logging.basicConfig(level=logging.INFO) once here, and for `compare`, print the
    Markdown table and save a CSV under reports/ (scorecard.write_csv).

    Hint: keep main() synchronous and bridge with asyncio.run(_run(args)).
    """
    args = build_parser().parse_args()
    raise NotImplementedError(f"command {args.command!r} is not implemented yet")


if __name__ == "__main__":  # lets `python -m doubleagent.cli` (and the VS Code debugger) run it
    main()
