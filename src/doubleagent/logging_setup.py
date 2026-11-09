"""One place that configures logging for the whole app.

C# analogy: `builder.Logging.AddConsole().SetMinimumLevel(...)` in Program.cs.
Library modules never configure logging; they only call `logging.getLogger(__name__)`
(≈ `ILogger<T>`) and log. The entry point (cli.py, the UI) calls `configure_logging` once.
"""

import logging

# time | level | logger name (= module, like the category in ILogger<T>) | message
LOG_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"

# Chatty third-party loggers. At INFO they repeat what our own logs say; at DEBUG we want them.
NOISY_LOGGERS = ("httpx", "httpx2", "httpcore", "anthropic")


def configure_logging(level: str = "INFO") -> None:
    """Send logs to stderr (stdout stays clean for answers) at `level`."""
    numeric = logging.getLevelNamesMapping()[level.upper()]
    # force=True replaces any earlier setup, so calling this twice is safe.
    logging.basicConfig(level=numeric, format=LOG_FORMAT, datefmt="%H:%M:%S", force=True)
    for name in NOISY_LOGGERS:
        logging.getLogger(name).setLevel(numeric if numeric <= logging.DEBUG else logging.WARNING)
