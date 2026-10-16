"""Terminal Processes of MT5 Service: the Terminals, MT5 Error, and the process that runs the Package."""

import math
import multiprocessing
import threading
from dataclasses import dataclass, field
from multiprocessing.connection import Connection
from multiprocessing.process import BaseProcess
from pathlib import Path
from types import ModuleType
from typing import Any

import yaml

type JSON = dict[str, JSON] | list[JSON] | str | int | float | bool | None

GENERIC_FAIL = -1
INVALID_PARAMS = -2

CONFIG = Path(__file__).with_name("config.yaml")
SECTIONS = ("general", "terminals")
FIELDS: dict[str, type] = {
    "name": str,
    "path": str,
    "username": str,
    "password": str,
    "investor_password": str,
    "ip": str,
    "port": int,
    "api_key": str,
    "description": str,
}
REQUIRED_FIELDS = ("name", "path")


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
    """One MetaTrader 5 terminal declared in config.yaml; an empty field is None."""

    name: str
    path: str | None = None
    username: str | None = None
    password: str | None = None
    investor_password: str | None = None
    ip: str | None = None
    port: int | None = None
    api_key: str | None = None
    description: str | None = None


def _entry_problems(label: str, entry: dict[object, object]) -> list[str]:
    """List every problem of one Terminal entry without echoing any field value."""
    problems: list[str] = []
    unknown = sorted(str(key) for key in entry if key not in FIELDS)
    if unknown:
        problems.append(f"{label} has unknown fields: {', '.join(unknown)}")
    for key in REQUIRED_FIELDS:
        if key not in entry:
            problems.append(f"{label} needs the field '{key}'")
    name = entry.get("name")
    if "name" in entry and (not isinstance(name, str) or not name.strip()):
        problems.append(f"{label} needs a non-empty string 'name'")
    for key, kind in FIELDS.items():
        value = entry.get(key)
        if key == "name" or value is None or (kind is str and value == ""):
            continue
        if not isinstance(value, kind) or isinstance(value, bool):
            problems.append(f"{label} field '{key}' must be {kind.__name__} or empty")
    return problems


def load_terminals() -> dict[str, Terminal]:
    """Read config.yaml, refusing it with every problem found when it is invalid."""
    try:
        text = CONFIG.read_text(encoding="utf-8")
    except OSError as error:
        raise MT5Error(
            GENERIC_FAIL, f"config.yaml cannot be read: {error.strerror}"
        ) from None
    try:
        document = yaml.safe_load(text)
    except yaml.YAMLError as error:
        mark = getattr(error, "problem_mark", None)
        where = f" at line {mark.line + 1}" if mark is not None else ""
        raise MT5Error(
            INVALID_PARAMS, f"config.yaml is not valid YAML{where}"
        ) from None
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
    if general is not None and not isinstance(general, dict):
        problems.append("the section 'general' must be a mapping")
    elif general:
        settings = ", ".join(sorted(str(key) for key in general))
        problems.append(f"the section 'general' has unknown settings: {settings}")
    entries = document.get("terminals")
    if entries is None:
        entries = []
    if not isinstance(entries, list):
        problems.append("the section 'terminals' must be a list of Terminal entries")
        entries = []
    first: dict[str, int] = {}
    for index, entry in enumerate(entries, start=1):
        label = f"terminal {index}"
        if not isinstance(entry, dict):
            problems.append(f"{label} is not a mapping")
            continue
        problems.extend(_entry_problems(label, entry))
        name = entry.get("name")
        if isinstance(name, str):
            if name in first:
                problems.append(f"{label} repeats the name of terminal {first[name]}")
            first.setdefault(name, index)
    if problems:
        raise MT5Error(INVALID_PARAMS, "config.yaml is invalid: " + "; ".join(problems))
    terminals: dict[str, Terminal] = {}
    for entry in entries:
        values: dict[str, Any] = {
            key: None if value == "" else value for key, value in entry.items()
        }
        terminals[entry["name"]] = Terminal(**values)
    return terminals


def resolve(terminal: object) -> Terminal:
    """Find the Terminal a caller names, refusing a name config.yaml does not declare."""
    if not isinstance(terminal, str):
        raise MT5Error(
            INVALID_PARAMS,
            "parameter 'terminal' must be the name of a Terminal in config.yaml",
        )
    found = load_terminals().get(terminal)
    if found is None:
        raise MT5Error(INVALID_PARAMS, f"Terminal '{terminal}' is not in config.yaml")
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
    if value is None or isinstance(value, str | bool | int | float):
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
        if package is None:
            pipe.send(("error", GENERIC_FAIL, unavailable))
        else:
            pipe.send(_run(package, function, args, kwargs))
        if function == "shutdown":
            return


@dataclass
class _Process:
    process: BaseProcess
    pipe: Connection
    lock: threading.Lock = field(default_factory=threading.Lock)


_context = multiprocessing.get_context("spawn")
_processes: dict[str, _Process] = {}
_registry = threading.Lock()


def _start(terminal: str) -> _Process:
    pipe, child = _context.Pipe()
    process = _context.Process(
        target=_serve, args=(child,), name=f"mt5-terminal-{terminal}", daemon=True
    )
    process.start()
    child.close()
    return _Process(process, pipe)


def _stop(terminal: str, running: _Process) -> None:
    with _registry:
        if _processes.get(terminal) is running:
            del _processes[terminal]
    running.pipe.close()
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
    of which those left as None are not sent, so the Package applies its own defaults.
    """
    resolve(terminal)
    positional = positional or {}
    named = {name: value for name, value in (named or {}).items() if value is not None}
    for name, value in {**positional, **named}.items():
        check_json(name, value)
    started = False
    with _registry:
        running = _processes.get(terminal)
        if running is None:
            if function != "initialize":
                raise MT5Error(
                    GENERIC_FAIL,
                    f"Terminal '{terminal}' is not initialized; call initialize first",
                )
            running = _processes[terminal] = _start(terminal)
            started = True
    with running.lock:
        try:
            running.pipe.send((function, list(positional.values()), named))
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
