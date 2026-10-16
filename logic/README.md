# Logic

## Overview

Logic is the reusable library that holds the Behavior of MT5 Interface in its Services and publishes every Service through one Logic Interface, so a consumer never depends on where a Service lives. It starts no process of its own and owns no transport.

```python
from logic.interface import MT5

MT5.Connection.initialize("demo")
```

## Interface

The Logic Interface, `logic.interface`, publishes exactly one name:

- `MT5` — the MT5 Service Interface.

## Services

- **MT5** — [README](logic/services/mt5/README.md) · [Definition](../.interface/implementation/development/logic/services/mt5/mt5.md) · [Preferences](../.interface/implementation/development/logic/services/mt5/mt5.yaml)

## Setup

Logic needs Python 3.14 and [uv](https://docs.astral.sh/uv/). From this directory:

```sh
uv sync
```

The MetaTrader5 package is installed only on Windows. Calling a Terminal through MT5 Service also needs MetaTrader 5 installed on the same machine and the Terminal declared in `logic/services/mt5/config.yaml`; its sample `demo` entry needs only its `path` filled in, and the [MT5 Service README](logic/services/mt5/README.md#use) shows how to add more. Reading `MT5.Constants` needs neither.

A consumer in this repository depends on Logic as a local path dependency on this directory.

## Use

Import a Service from the Logic Interface and use what it publishes:

```python
from logic.interface import MT5

MT5.Connection.initialize("demo")
bars = MT5.MarketData.copy_rates_from_pos(
    "demo", "EURUSD", MT5.Constants.TIMEFRAME_H1, 0, 10
)
MT5.Connection.shutdown("demo")
```

## Verify

```sh
uv run python -c "import logic.interface as L; print(L.__all__)"
```

prints `['MT5']`, and `L.MT5` is the module `logic.services.mt5.interface` itself.

## Troubleshooting

- **`RuntimeError: An attempt has been made to start a new process before the current process has finished its bootstrapping phase`** — MT5 Service runs the package in separate processes started with `spawn`. Put the code that calls MT5 Service under `if __name__ == "__main__":` in the script you run.
- **`MT5Error (-1) The MetaTrader5 package is unavailable`** — raised by a call to a Terminal, because the package is installed only on Windows. Run on Windows with `uv sync`.
- **`MT5Error (-2) Terminal 'X' is not in config.yaml`** — add an entry with that `name` to the `terminals` section of `logic/services/mt5/config.yaml`, or use a configured name.
- **`MT5Error (-2) Terminal 'X' has no path in config.yaml`** — fill in that Terminal's `path`, as for the sample `demo` entry.
- **`MT5Error (-2) config.yaml is invalid: ...`** — fix every listed problem: keep exactly the `general` and `terminals` sections; every entry has a `name` and a `path`; names are unique; only the documented fields are allowed; `port` is an integer and every other field is a string (quote numeric passwords), or left empty.
- **`MT5Error (-1) Terminal 'X' is not initialized`** — call `Connection.initialize` for that Terminal first; `shutdown` ends its process.
