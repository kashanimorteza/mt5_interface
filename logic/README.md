# Logic

## Overview

Logic is the reusable library that holds the Behavior of MT5 Interface in its Services and publishes every Service through one Logic Interface, so a consumer never depends on where a Service lives. It starts no process of its own and owns no transport.

```python
from logic.interface import MT5

demo = MT5("demo")
print(demo.Connection.terminal_info())
```

## Interface

The Logic Interface, `logic.interface`, publishes exactly one name:

- `MT5` — the `MT5` class of MT5 Service, the one name that Service publishes; it also carries `MT5.Constants` and `MT5.Error`.

## Services

- **MT5** — [README](logic/services/mt5/README.md) · [Definition](../.interface/implementation/development/logic/services/mt5/mt5.md) · [Preferences](../.interface/implementation/development/logic/services/mt5/mt5.yaml)

## Setup

Logic needs Python 3.14 and [uv](https://docs.astral.sh/uv/). From this directory:

```sh
uv sync
```

Logic installs on every operating system. The MetaTrader5 package is installed only on Windows; elsewhere, every call to a Terminal raises `MT5.Error`. Calling a Terminal through MT5 Service needs MetaTrader 5 installed on the same machine and the Terminal declared, keyed by its name, in the `terminals` section of `logic/services/mt5/config.yaml`; its sample `demo` Terminal needs only its `path` filled in, and the [MT5 Service README](logic/services/mt5/README.md#use) shows how to add more. Reading `MT5.Constants` needs neither.

A consumer in this repository depends on Logic as a local path dependency on this directory.

## Use

Import a Service from the Logic Interface and use what it publishes. For MT5, create an MT5 instance for a Terminal and call its Function Groups:

```python
from logic.interface import MT5

demo = MT5("demo")
bars = demo.MarketData.copy_rates_from_pos("EURUSD", MT5.Constants.TIMEFRAME_H1, 0, 10)
```

## Verify

```sh
uv run python -c "import logic.interface as L; print(L.__all__)"
```

prints `['MT5']`, and `L.MT5` is the `MT5` class of MT5 Service itself, because MT5 Service publishes exactly that one name.

## Troubleshooting

- **`RuntimeError: An attempt has been made to start a new process before the current process has finished its bootstrapping phase`** — MT5 Service runs the package in separate processes started with `spawn`. Put the code that calls MT5 Service under `if __name__ == "__main__":` in the script you run.
- **`MT5.Error (-1) The MetaTrader5 package is unavailable`** — raised by `initialize` on a machine where the package is not installed, because it is installed only on Windows. Run on Windows with `uv sync`.
- **`MT5.Error (-2) Terminal 'X' is not in config.yaml`** — raised when creating an MT5 instance, or by a call, for a name that is not a key of the `terminals` section of `logic/services/mt5/config.yaml`; add that Terminal under its name, or use a configured name.
- **`MT5.Error (-2) Terminal 'X' has no path in config.yaml`** — fill in that Terminal's `path`, as for the sample `demo` entry.
- **`MT5.Error (-2) config.yaml is invalid: ...`** — fix every listed problem: keep exactly the `general` and `terminals` sections; `terminals` maps each Terminal's name to its fields, never a list; every Terminal lists exactly the documented fields; `port` is an integer and every other field is a string (quote numeric passwords), or left empty.
- **`MT5.Error (-2) config.yaml repeats a key at line N`** — two Terminals share a name, or one Terminal repeats a field; keep each once.
- **`MT5.Error (-1) Terminal 'X' is not initialized`** — no Terminal Process is running for that Terminal; its `Connection.initialize()` starts one, and its `shutdown` ends it for every instance of that Terminal.
- **`MT5.Error (-10005) Terminal 'X' did not answer ... within N seconds`** — the Terminal did not answer within `call_timeout` of the `general` section of `logic/services/mt5/config.yaml`; its process was ended, so call `Connection.initialize()` again, or raise `call_timeout`.
