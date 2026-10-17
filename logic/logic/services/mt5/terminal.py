"""Terminal Processes of MT5 Service: the Terminals, MT5 Error, and the process that runs the Package."""

import atexit
import math
import multiprocessing
import threading
from collections.abc import Hashable
from dataclasses import dataclass, field
from multiprocessing.connection import Connection
from multiprocessing.process import BaseProcess
from pathlib import Path
from types import ModuleType
from typing import Any

import yaml
from yaml.constructor import ConstructorError

from logic.services.mt5.constants import Constants

type JSON = dict[str, JSON] | list[JSON] | str | int | float | bool | None

GENERIC_FAIL = Constants.RES_E_FAIL
INVALID_PARAMS = Constants.RES_E_INVALID_PARAMS
TIMEOUT = Constants.RES_E_INTERNAL_FAIL_TIMEOUT

CONFIG = Path(__file__).with_name("config.yaml")
SECTIONS = ("general", "terminals")
GENERAL: dict[str, type] = {"call_timeout": int}
FIELDS: dict[str, type] = {
    "path": str,
    "username": str,
    "password": str,
    "investor_password": str,
    "ip": str,
    "port": int,
    "api_key": str,
    "description": str,
}


class MT5Error(Exception):
    """The one error MT5 Service raises, carrying the Package's error code and message."""

    def __init__(self, code: int, message: str) -> None:
        super().__init__(code, message)
        self.code = code
        self.message = message

    def __str__(self) -> str:
        return f"({self.code}) {self.message}"


@dataclass(frozen=True)
class Terminal:
    """One MetaTrader 5 terminal declared in config.yaml; an empty field is None.

    Secret fields are left out of its representation, so they never reach a message or a log.
    """

    name: str
    path: str | None = None
    username: str | None = None
    password: str | None = field(default=None, repr=False)
    investor_password: str | None = field(default=None, repr=False)
    ip: str | None = None
    port: int | None = None
    api_key: str | None = field(default=None, repr=False)
    description: str | None = None


@dataclass(frozen=True)
class Configuration:
    """Terminal Configuration as read from config.yaml."""

    call_timeout: int
    terminals: dict[str, Terminal]


REPEATED_KEY = "found a repeated key"


class _UniqueKeyLoader(yaml.SafeLoader):
    """A safe YAML loader that refuses a mapping repeating a key, such as a Terminal name."""

    def construct_mapping(
        self, node: yaml.MappingNode, deep: bool = False
    ) -> dict[Any, Any]:
        seen: set[object] = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, Hashable):
                continue
            if key in seen:
                raise ConstructorError(None, None, REPEATED_KEY, key_node.start_mark)
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


def _entry_problems(label: str, entry: dict[object, object]) -> list[str]:
    """List every problem of one Terminal entry without echoing any field value."""
    problems: list[str] = []
    unknown = sorted(str(key) for key in entry if key not in FIELDS)
    if unknown:
        problems.append(f"{label} has unknown fields: {', '.join(unknown)}")
    missing = [key for key in FIELDS if key not in entry]
    if missing:
        problems.append(f"{label} misses the fields: {', '.join(missing)}")
    for key, kind in FIELDS.items():
        value = entry.get(key)
        if value is None or (kind is str and value == ""):
            continue
        if not isinstance(value, kind) or isinstance(value, bool):
            problems.append(f"{label} field '{key}' must be {kind.__name__} or empty")
    return problems


def _read() -> Configuration:
    """Read config.yaml, refusing it with every problem found when it is invalid."""
    try:
        text = CONFIG.read_text(encoding="utf-8")
    except OSError as error:
        raise MT5Error(
            GENERIC_FAIL, f"config.yaml cannot be read: {error.strerror}"
        ) from None
    try:
        document = yaml.load(text, Loader=_UniqueKeyLoader)
    except yaml.YAMLError as error:
        mark = getattr(error, "problem_mark", None)
        where = f" at line {mark.line + 1}" if mark is not None else ""
        problem = (
            "repeats a key"
            if getattr(error, "problem", None) == REPEATED_KEY
            else "is not valid YAML"
        )
        raise MT5Error(INVALID_PARAMS, f"config.yaml {problem}{where}") from None
    if not isinstance(document, dict):
        raise MT5Error(
            INVALID_PARAMS, "config.yaml must hold the sections general and terminals"
        )
    problems: list[str] = []
    for section in SECTIONS:
        if section not in document:
            problems.append(f"the section '{section}' is missing")
    unknown = sorted(str(key) for key in document if key not in SECTIONS)
    if unknown:
        problems.append(f"unknown sections: {', '.join(unknown)}")
    general = document.get("general")
    if not isinstance(general, dict):
        problems.append("the section 'general' must be a mapping")
        general = {}
    unknown_settings = sorted(str(key) for key in general if key not in GENERAL)
    if unknown_settings:
        problems.append(
            f"the section 'general' has unknown settings: {', '.join(unknown_settings)}"
        )
    timeout = general.get("call_timeout")
    if not isinstance(timeout, int) or isinstance(timeout, bool) or timeout <= 0:
        problems.append(
            "the setting 'call_timeout' must be a positive whole number of seconds"
        )
    entries = document.get("terminals")
    if entries is None:
        entries = {}
    if not isinstance(entries, dict):
        problems.append(
            "the section 'terminals' must be a mapping from Terminal name to its fields"
        )
        entries = {}
    for index, (name, entry) in enumerate(entries.items(), start=1):
        if not isinstance(name, str) or not name.strip():
            problems.append(
                f"terminal {index} needs a non-empty string name as its key"
            )
            continue
        label = f"terminal {index}"
        if not isinstance(entry, dict):
            problems.append(f"{label} is not a mapping of fields")
            continue
        problems.extend(_entry_problems(label, entry))
    if problems:
        raise MT5Error(INVALID_PARAMS, "config.yaml is invalid: " + "; ".join(problems))
    terminals: dict[str, Terminal] = {}
    for name, entry in entries.items():
        values: dict[str, Any] = {
            key: None if value == "" else value for key, value in entry.items()
        }
        terminals[name] = Terminal(name, **values)
    assert isinstance(timeout, int)
    return Configuration(timeout, terminals)


_cache: tuple[tuple[int, int], Configuration] | None = None
_cache_lock = threading.Lock()


def configuration() -> Configuration:
    """Return Terminal Configuration, reading config.yaml again only when it has changed."""
    global _cache
    try:
        status = CONFIG.stat()
    except OSError as error:
        raise MT5Error(
            GENERIC_FAIL, f"config.yaml cannot be read: {error.strerror}"
        ) from None
    stamp = (status.st_mtime_ns, status.st_size)
    with _cache_lock:
        if _cache is None or _cache[0] != stamp:
            _cache = (stamp, _read())
        return _cache[1]


def load_terminals() -> dict[str, Terminal]:
    """Return every Terminal of Terminal Configuration by its name."""
    return configuration().terminals


def find(terminal: object) -> Terminal:
    """Find the Terminal a caller names, refusing a name config.yaml does not declare."""
    if not isinstance(terminal, str):
        raise MT5Error(
            INVALID_PARAMS,
            "parameter 'terminal' must be the name of a Terminal in config.yaml",
        )
    found = load_terminals().get(terminal)
    if found is None:
        raise MT5Error(INVALID_PARAMS, f"Terminal '{terminal}' is not in config.yaml")
    return found


def resolve(terminal: object) -> Terminal:
    """Find the Terminal a call is for, refusing an unknown name or a Terminal without a path."""
    found = find(terminal)
    if found.path is None:
        raise MT5Error(
            INVALID_PARAMS, f"Terminal '{terminal}' has no path in config.yaml"
        )
    return found


def check_json(name: str, value: object) -> None:
    """Refuse a parameter that is not a JSON value."""
    if value is None or isinstance(value, str | bool | int):
        return
    if isinstance(value, float) and math.isfinite(value):
        return
    if isinstance(value, list):
        for item in value:
            check_json(name, item)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                break
            check_json(name, item)
        else:
            return
    raise MT5Error(INVALID_PARAMS, f"parameter '{name}' is not a JSON value")


def check_timestamp(name: str, value: object) -> None:
    """Refuse a date and time that is not a Timestamp, a whole number of seconds since 1970-01-01 UTC."""
    if value is None or (isinstance(value, int) and not isinstance(value, bool)):
        return
    raise MT5Error(
        INVALID_PARAMS,
        f"parameter '{name}' must be a Timestamp in whole seconds since 1970-01-01 UTC",
    )


def plain(value: Any) -> JSON:
    """Convert a Package result to Plain Data, keeping its field names and values."""
    if hasattr(value, "_asdict"):
        return {str(key): plain(item) for key, item in value._asdict().items()}
    names = getattr(getattr(value, "dtype", None), "names", None)
    if names:
        return [
            dict(zip(names, (plain(item) for item in row), strict=True))
            for row in value.tolist()
        ]
    if hasattr(value, "tolist"):
        return plain(value.tolist())
    if isinstance(value, list | tuple):
        return [plain(item) for item in value]
    if isinstance(value, dict):
        return {str(key): plain(item) for key, item in value.items()}
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if value is None or isinstance(value, str | bool | int):
        return value
    raise MT5Error(
        GENERIC_FAIL,
        f"the Package returned a value of type {type(value).__name__} that is not Plain Data",
    )


type Outcome = tuple[str, JSON] | tuple[str, int, str]


def _run(
    package: ModuleType, function: str, args: list[JSON], kwargs: dict[str, JSON]
) -> Outcome:
    """Call one Function of the Package and turn its result or failure into an Outcome."""
    try:
        result = getattr(package, function)(*args, **kwargs)
    except TypeError as error:
        return ("error", INVALID_PARAMS, str(error))
    except Exception as error:  # noqa: BLE001 - every Package failure becomes MT5 Error
        return ("error", GENERIC_FAIL, f"{type(error).__name__}: {error}")
    if result is False or (result is None and function != "shutdown"):
        code, message = package.last_error()
        return ("error", code, message)
    try:
        return ("result", plain(result))
    except MT5Error as error:
        return ("error", error.code, error.message)


def _serve(pipe: Connection) -> None:
    """Run the Package for one Terminal, answering its calls one after another until shutdown."""
    package: ModuleType | None
    try:
        import MetaTrader5 as package  # ty: ignore[unresolved-import]
    except ImportError as error:
        package = None
        unavailable = f"The MetaTrader5 package is unavailable: {error}"
    while True:
        try:
            function, args, kwargs = pipe.recv()
        except EOFError:
            return
        outcome = (
            ("error", GENERIC_FAIL, unavailable)
            if package is None
            else _run(package, function, args, kwargs)
        )
        try:
            pipe.send(outcome)
        except OSError:
            return
        if function == "shutdown":
            return


@dataclass
class _Process:
    process: BaseProcess
    pipe: Connection


_context = multiprocessing.get_context("spawn")
_processes: dict[str, _Process] = {}
_locks: dict[str, threading.Lock] = {}
_registry = threading.Lock()


def _lock(terminal: str) -> threading.Lock:
    """Return the lock that serializes everything for one Terminal, creating it once."""
    with _registry:
        return _locks.setdefault(terminal, threading.Lock())


def _start(terminal: str) -> _Process:
    pipe, child = _context.Pipe()
    process = _context.Process(
        target=_serve, args=(child,), name=f"mt5-terminal-{terminal}", daemon=True
    )
    process.start()
    child.close()
    return _Process(process, pipe)


def _stop(terminal: str, running: _Process, force: bool = False) -> None:
    """Remove a Terminal Process from the registry and end it, at once when it is forced."""
    with _registry:
        if _processes.get(terminal) is running:
            del _processes[terminal]
    running.pipe.close()
    if not force:
        running.process.join(timeout=5)
    if running.process.is_alive():
        running.process.terminate()
        running.process.join()


def call(
    terminal: str,
    function: str,
    positional: dict[str, JSON] | None = None,
    named: dict[str, JSON] | None = None,
) -> JSON:
    """Run one Function of the Package in the Terminal Process of the named Terminal.

    `positional` holds the Function's unnamed parameters in order; `named` holds its named parameters,
    of which those left as None are not sent, so the Package applies its own defaults. A call that is
    not answered within the Call Timeout raises MT5 Error and ends the Terminal Process.
    """
    resolve(terminal)
    timeout = configuration().call_timeout
    positional = positional or {}
    named = {name: value for name, value in (named or {}).items() if value is not None}
    for name, value in {**positional, **named}.items():
        check_json(name, value)
    started = False
    with _lock(terminal):
        with _registry:
            running = _processes.get(terminal)
        if running is None:
            if function != "initialize":
                raise MT5Error(
                    GENERIC_FAIL,
                    f"Terminal '{terminal}' is not initialized; call initialize first",
                )
            running = _start(terminal)
            with _registry:
                _processes[terminal] = running
            started = True
        try:
            running.pipe.send((function, list(positional.values()), named))
            if not running.pipe.poll(timeout):
                _stop(terminal, running, force=True)
                raise MT5Error(
                    TIMEOUT,
                    f"Terminal '{terminal}' did not answer {function} within {timeout} seconds",
                )
            outcome = running.pipe.recv()
        except EOFError, OSError:
            _stop(terminal, running)
            raise MT5Error(
                GENERIC_FAIL, f"The process of Terminal '{terminal}' ended unexpectedly"
            ) from None
        if function == "shutdown" or (started and outcome[0] == "error"):
            _stop(terminal, running)
    if outcome[0] == "error":
        raise MT5Error(outcome[1], outcome[2])
    return outcome[1]


def _shutdown_all() -> None:
    """Shut down every running Terminal when the Owner Process ends normally."""
    with _registry:
        running = list(_processes)
    for terminal in running:
        try:
            call(terminal, "shutdown")
        except MT5Error:
            with _registry:
                leftover = _processes.get(terminal)
            if leftover is not None:
                _stop(terminal, leftover)


atexit.register(_shutdown_all)
