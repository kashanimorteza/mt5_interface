# Logic

## Overview

Logic is the reusable library that holds the Behavior of MT5 Interface in its Services and publishes every Service through one Logic Interface, so a consumer never depends on where a Service lives. It starts no process of its own and owns no transport.

```python
from logic.interface import MT5

MT5.Connection.initialize("Demo")
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

The MetaTrader5 package is installed only on Windows. Using MT5 Service also needs MetaTrader 5 installed on the same machine and each Terminal listed in `logic/services/mt5/terminal.config`.

A consumer in this repository depends on Logic as a local path dependency on this directory.

## Use

Import a Service from the Logic Interface and use what it publishes:

```python
from logic.interface import MT5

MT5.Connection.initialize("Demo")
bars = MT5.MarketData.copy_rates_from_pos(
    "Demo", "EURUSD", MT5.Constants.TIMEFRAME_H1, 0, 10
)
MT5.Connection.shutdown("Demo")
```

## Verify

```sh
uv run python -c "import logic.interface as L; print(L.__all__)"
```

prints `['MT5']`, and `L.MT5` is the module `logic.services.mt5.interface` itself.

## Troubleshooting

- **`RuntimeError: An attempt has been made to start a new process before the current process has finished its bootstrapping phase`** — MT5 Service runs the package in separate processes started with `spawn`. Put the code that calls MT5 Service under `if __name__ == "__main__":` in the script you run.
- **`MT5Error (-1) The MetaTrader5 package is unavailable`** — the package is installed only on Windows. Run on Windows with `uv sync`.
- **`MT5Error (-2) Terminal 'X' is not in terminal.config`** — add an entry with that `name` to `logic/services/mt5/terminal.config`, or use a configured name.
- **`MT5Error (-2) terminal.config is invalid: ...`** — fix every listed entry: `name` and `path` are required, names are unique, only the documented fields are allowed, and every value is a string (quote numeric passwords).
- **`MT5Error (-1) Terminal 'X' is not initialized`** — call `Connection.initialize` for that Terminal first; `shutdown` ends its process.
