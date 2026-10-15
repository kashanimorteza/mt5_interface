"""Terminal: MT5 Error, Plain Data, JSON parameters, and the Terminal Process in which the Package runs for each Terminal."""

import hashlib
import math
import multiprocessing
import multiprocessing.connection
import os
import pickle
import sys
import tempfile
import threading
from multiprocessing.connection import Client, Connection, Listener
from pathlib import Path
from typing import Any

# --- MT5 Error --------------------------------------------------------------------------


class MT5Error(Exception):
    """The one error MT5 Service raises when the Package reports a failure."""

    def __init__(self, code: int, message: str) -> None:
        super().__init__(code, message)
        self.code = code
        self.message = message

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


# --- Plain Data -------------------------------------------------------------------------

_PLAIN = (type(None), bool, int, str)


def _finite(value: float) -> float:
    if not math.isfinite(value):
        raise ValueError(
            f"A Package result holds the number {value!r}, which has no JSON form"
        )
    return value


def _name(name: Any) -> str:
    if type(name) is not str:
        raise TypeError(
            f"A Package result holds a {type(name).__name__} key, which has no JSON form"
        )
    return name


def plain(value: Any) -> Any:
    """Return a Package result as Plain Data, a valid JSON value, changing only its form, never its values or field names."""
    if type(value) in _PLAIN:
        return value
    if type(value) is float:
        return _finite(value)
    if hasattr(value, "_asdict"):
        return {_name(name): plain(item) for name, item in value._asdict().items()}
    if isinstance(value, dict):
        return {_name(name): plain(item) for name, item in value.items()}
    dtype = getattr(value, "dtype", None)
    if dtype is not None and hasattr(value, "tolist"):
        listed = value.tolist()
        names = dtype.names
        if names is None:
            return plain(listed)
        if isinstance(listed, tuple):
            return dict(zip(names, (plain(item) for item in listed), strict=True))
        return [
            dict(zip(names, (plain(item) for item in row), strict=True))
            for row in listed
        ]
    if isinstance(value, (tuple, list)):
        return [plain(item) for item in value]
    if isinstance(value, bool):
        return bool(value)
    if isinstance(value, int):
        return int(value)
    if isinstance(value, float):
        return _finite(float(value))
    if isinstance(value, str):
        return str(value)
    raise TypeError(
        f"A Package result of type {type(value).__name__} has no Plain Data form"
    )


# --- JSON Parameters --------------------------------------------------------------------

# The Package's own last_error code for invalid parameters, used when a value is refused before any call.
_INVALID_PARAMS = -2

_TIMESTAMPS = frozenset({"date_from", "date_to"})
"""The parameters the Package Documentation sets by a date and time; the Package takes each as a Timestamp."""


def _json(value: Any) -> bool:
    if value is None or type(value) in (bool, int, str):
        return True
    if type(value) is float:
        return math.isfinite(value)
    if type(value) is list:
        return all(_json(item) for item in value)
    if type(value) is dict:
        return all(type(name) is str and _json(item) for name, item in value.items())
    return False


def _parameter(name: str, value: Any) -> Any:
    """One parameter in the form the Package takes, or MT5 Error when it is not a JSON value."""
    if name in _TIMESTAMPS:
        if type(value) is int:
            return value
        if type(value) is float and value.is_integer():
            return int(value)
        raise MT5Error(
            _INVALID_PARAMS,
            f"{name} is not a Timestamp: a whole number of seconds since 1970-01-01 00:00:00 UTC",
        )
    if not _json(value):
        raise MT5Error(_INVALID_PARAMS, f"{name} is not a JSON value")
    return value


def given(**values: Any) -> tuple:
    """The unnamed parameters a caller supplied, in order up to the last one given, as the Package takes them; one left out before it is sent as None."""
    items = list(values.items())
    while items and items[-1][1] is None:
        items.pop()
    return tuple(
        None if value is None else _parameter(name, value) for name, value in items
    )


def named(**values: Any) -> dict[str, Any]:
    """The named parameters a caller supplied, as the Package takes them."""
    return {
        name: _parameter(name, value)
        for name, value in values.items()
        if value is not None
    }


def _terminal(terminal: Any) -> str:
    if type(terminal) is not str:
        raise MT5Error(_INVALID_PARAMS, "terminal is not a JSON string")
    return terminal


# --- Terminal Processes -----------------------------------------------------------------

_CONTEXT = multiprocessing.get_context("spawn")
_START_TIMEOUT = 60.0

# Codes of the Package's own last_error table, used where no Package call could report one.
_INTERNAL_FAIL_RECEIVE = -10002
_INTERNAL_FAIL_INIT = -10003
_INTERNAL_FAIL_CONNECT = -10004
_INTERNAL_FAIL_TIMEOUT = -10005

_OPENING_LOCK = threading.Lock()
_OPENING: dict[str, threading.Lock] = {}
_OWNED: dict[str, Any] = {}


class _Absent(Exception):
    """No Terminal Process answers at a Terminal's address."""


def _address(terminal: str) -> str:
    name = "mt5-terminal-" + hashlib.sha256(terminal.encode("utf-8")).hexdigest()[:32]
    if sys.platform == "win32":
        return rf"\\.\pipe\{name}"
    return str(Path(tempfile.gettempdir()) / f"{name}.sock")


def _authkey() -> bytes:
    return bytes(multiprocessing.current_process().authkey)


def _sendable(error: Exception) -> Exception:
    try:
        pickle.loads(pickle.dumps(error))
    except Exception:  # noqa: BLE001 - any error that cannot cross the process boundary is described instead
        return RuntimeError(f"{type(error).__name__}: {error}")
    return error


def _run(
    package: Any, function: str, args: tuple, kwargs: dict, failures: tuple
) -> tuple:
    try:
        result = getattr(package, function)(*args, **kwargs)
        if any(result is failure for failure in failures):
            code, message = package.last_error()
            return ("failure", code, message)
        return ("result", plain(result))
    except Exception as error:  # noqa: BLE001 - every Package exception reaches the caller unchanged
        return ("raised", _sendable(error))


def _end_with(sentinel: Any, address: str) -> None:
    """End the Terminal Process as soon as the caller process that started it ends, however it ends."""
    multiprocessing.connection.wait([sentinel])
    if sys.platform != "win32":
        Path(address).unlink(missing_ok=True)
    os._exit(0)


def _serve(address: str, authkey: bytes, ready: Connection) -> None:
    """The Terminal Process: loads the Package and runs every call for its Terminal, one after another."""
    try:
        listener = Listener(address, authkey=authkey)
    except OSError:
        ready.send(("taken", None))
        return
    with listener:
        try:
            import MetaTrader5 as mt5  # ty: ignore[unresolved-import] - installed on Windows only
        except ImportError as error:
            ready.send(("unavailable", f"{type(error).__name__}: {error}"))
            return
        ready.send(("ready", None))
        ready.close()
        starter = multiprocessing.parent_process()
        if starter is not None:
            threading.Thread(
                target=_end_with, args=(starter.sentinel, address), daemon=True
            ).start()
        opened = False
        while True:
            try:
                connection = listener.accept()
            except multiprocessing.AuthenticationError, OSError, EOFError:
                continue
            with connection:
                try:
                    function, args, kwargs, failures = connection.recv()
                except OSError, EOFError:
                    continue
                reply = _run(mt5, function, args, kwargs, failures)
                if function == "initialize" and reply[0] == "result":
                    opened = True
                ending = function == "shutdown" or (
                    function == "initialize" and not opened
                )
                try:
                    connection.send((ending, *reply))
                except OSError:
                    pass
            if ending:
                return


def _request(terminal: str, message: tuple) -> tuple:
    try:
        connection = Client(_address(terminal), authkey=_authkey())
    except FileNotFoundError, ConnectionRefusedError:
        raise _Absent from None
    with connection:
        connection.send(message)
        try:
            return connection.recv()
        except EOFError:
            raise MT5Error(
                _INTERNAL_FAIL_RECEIVE,
                "The Terminal Process ended before answering",
            ) from None


def _clear_stale(address: str) -> None:
    if not Path(address).exists():
        return
    try:
        Client(address, authkey=_authkey()).close()
    except ConnectionRefusedError:
        Path(address).unlink(missing_ok=True)


def _start(terminal: str) -> None:
    address = _address(terminal)
    if sys.platform != "win32":
        _clear_stale(address)
    receiving, sending = _CONTEXT.Pipe(duplex=False)
    process = _CONTEXT.Process(
        target=_serve,
        args=(address, _authkey(), sending),
        name="mt5-terminal",
        daemon=True,
    )
    process.start()
    sending.close()
    with receiving:
        if not receiving.poll(_START_TIMEOUT):
            process.kill()
            raise MT5Error(
                _INTERNAL_FAIL_TIMEOUT, "The Terminal Process did not start in time"
            )
        state, detail = receiving.recv()
    if state == "ready":
        _OWNED[terminal] = process
        return
    process.join()
    if state == "unavailable":
        raise MT5Error(
            _INTERNAL_FAIL_INIT, f"The MetaTrader5 package cannot be loaded ({detail})"
        )


def _answer(terminal: str, reply: tuple) -> Any:
    ending, kind, *payload = reply
    if ending:
        process = _OWNED.pop(terminal, None)
        if process is not None:
            process.join(_START_TIMEOUT)
    if kind == "result":
        return payload[0]
    if kind == "failure":
        raise MT5Error(payload[0], payload[1])
    raise payload[0]


def open(terminal: str, args: tuple, kwargs: dict, failures: tuple) -> Any:
    """Open a Terminal: start its Terminal Process when it has none, then run the opening Function in it."""
    terminal = _terminal(terminal)
    message = ("initialize", args, kwargs, failures)
    with _OPENING_LOCK:
        lock = _OPENING.setdefault(terminal, threading.Lock())
    with lock:
        try:
            reply = _request(terminal, message)
        except _Absent:
            _start(terminal)
            try:
                reply = _request(terminal, message)
            except _Absent:
                raise MT5Error(
                    _INTERNAL_FAIL_CONNECT,
                    "The Terminal Process could not be reached after it started",
                ) from None
    return _answer(terminal, reply)


def call(
    terminal: str, function: str, args: tuple, kwargs: dict, failures: tuple
) -> Any:
    """Run one Function in the Terminal Process of its Terminal and return its result as Plain Data."""
    terminal = _terminal(terminal)
    try:
        reply = _request(terminal, (function, args, kwargs, failures))
    except _Absent:
        raise MT5Error(
            _INTERNAL_FAIL_CONNECT,
            "This Terminal has no running Terminal Process; open it first",
        ) from None
    return _answer(terminal, reply)
