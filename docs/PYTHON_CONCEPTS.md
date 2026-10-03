# Python concepts map

Where each language feature and standard-library module is introduced. ✅ = used in an exercise
that's already in the repo; the others arrive with their module. Each row says what it's like in C#.

## Language features

| Concept | C# counterpart | Lesson |
|---------|----------------|--------|
| Modules, packages, `import`, `src/` layout | namespaces, assemblies, `using` | 1.1 ✅ |
| Type hints, `X \| None`, `list[str]`, `dict[str, T]` | static types, `T?`, `List<T>`, `Dictionary<K,V>` | 1.1 ✅ |
| Functions, keyword-only args (`*,`), defaults | named/optional parameters | 1.1 ✅ |
| `async def` / `await`, `asyncio.run` | `async Task<T>`, `await`, async `Main` | 1.1 ✅ |
| `async with` (async context managers) | `await using` | 1.1 ✅ |
| Classes, `__init__`, `@classmethod` | constructors, static factory methods | 1.2 ✅ |
| f-strings, format specs (`:.0%`, `:.6f`) | string interpolation, format strings | 1.3 ✅ |
| List/dict/set comprehensions, generator expressions | LINQ `Select`/`Where` | 1.2 ✅ |
| Exceptions: `raise`, `try/except`, custom exception classes | `throw`, `try/catch`, custom exceptions | 1.2 ✅ |
| `match` statement (structural pattern matching) | `switch` expressions, patterns | 1.2 ✅ (CLI) |
| `Literal` types | string enums / closed sets | 1.2 ✅ |
| `@dataclass(frozen=True, slots=True)` | `record` | 1.3 ✅ |
| Truthiness, `any`/`all`, `sum` over booleans | `Any()`, `All()`, `Count()` | 1.3 ✅ |
| Closures, nested functions, functions as values | lambdas, `Func<T>` | 1.3 ✅ |
| Decorators (`@lru_cache`, `@tool`, your own) | attributes + interceptors | 1.1 ✅, 1.4, 3 |
| `enum.Enum`, `StrEnum` | `enum` | 2 |
| Generators and `yield` | `IEnumerable<T>` + `yield return` | 2 |
| `Protocol` (structural typing), ABCs | interfaces | 2 |
| Generics: `TypeVar`, `class Repo[T]` (3.12 syntax) | `class Repo<T>` | 3 |
| Context managers you write (`__enter__`, `@contextmanager`) | `IDisposable` | 3 |
| Async iterators, `async for`, `async` generators | `IAsyncEnumerable<T>`, `await foreach` | 3 (streaming) |
| `TypedDict`, `Annotated` | DTO shapes, attributes on parameters | 4 (LangGraph state) |
| `asyncio.TaskGroup`, `gather`, timeouts, cancellation | `Task.WhenAll`, `CancellationToken` | 4 |
| Dunder methods (`__repr__`, `__eq__`, `__hash__`) | `ToString`, `Equals`, `GetHashCode` | 5 |
| Packaging, entry points, `__main__` | console app, `Main` | 1.1 ✅, 7 |

## Standard library

| Module | Use in DoubleAgent | C# counterpart | Lesson |
|--------|-------------------|----------------|--------|
| `asyncio` | run async code, concurrent model calls | `System.Threading.Tasks` | 1.1 ✅, 1.3 ✅ |
| `argparse` | CLI subcommands | `System.CommandLine` | 1.1 ✅ |
| `functools` (`lru_cache`, `partial`) | cached settings | `Lazy<T>` | 1.1 ✅ |
| `json` | tool results, data files | `System.Text.Json` | 1.2 ✅ |
| `pathlib` | file paths | `System.IO.Path`/`FileInfo` | 1.2 ✅ |
| `datetime` | `last_updated` dates, freshness checks | `DateOnly`, `DateTime` | 1.2 ✅, 2 |
| `logging` | log tool calls | `ILogger<T>` | 1.2 ✅ |
| `typing`, `collections.abc` | `Literal`, `Sequence`, `Any` | generics, interfaces | 1.1 ✅ |
| `time` | latency via `perf_counter` | `Stopwatch` | 1.3 ✅ |
| `csv` | scorecard export | CsvHelper | 1.3 ✅ |
| `dataclasses` | value objects | records | 1.3 ✅ |
| `copy` | deep copies in test fakes | cloning | 1.1 ✅ (tests) |
| `re` | chunking, redaction, link parsing in the LLM Wiki | `Regex` | 2 |
| `hashlib` | content hashes for freshness, proposal versions | `SHA256` | 2, 5 |
| `itertools` | batching, chunk windows | LINQ `Chunk`, `Zip` | 2 |
| `collections` (`Counter`, `defaultdict`, `deque`) | BM25 term counts, histories | `Dictionary`, `Queue` | 2 |
| `math`, `statistics` | cosine similarity, median latency | `Math`, LINQ aggregates | 2, 6 |
| `sqlite3` | local vector/keyword store, activity log | `Microsoft.Data.Sqlite` | 2, 5 |
| `uuid` | idempotency keys, request ids | `Guid` | 3 |
| `contextlib` | `asynccontextmanager`, `suppress` | `using` helpers | 3 |
| `enum` | statuses, routes | `enum` | 2, 4 |
| `secrets` | approval tokens | `RandomNumberGenerator` | 5 |
| `os` | environment access (behind settings) | `Environment` | 7 |
| `unittest.mock` | `AsyncMock`, patching | Moq/NSubstitute | 3 |
| `tomllib` | reading `pyproject.toml` config | config providers | 7 |
| `concurrent.futures` | running blocking code from async | `Task.Run` | 4 |
