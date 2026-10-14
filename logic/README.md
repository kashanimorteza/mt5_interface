# Logic

## Overview

Logic is the project's reusable library of Behavior. Its work is divided into Services, each owning one responsibility, and Logic Interface publishes every Service's own Interface under the Service's name, so a consumer finds every Service in one place without knowing where it lives inside Logic. Logic runs no server and owns no transport; the API Component uses it as a library. Its MT5 Service runs the MetaTrader 5 package in one Terminal Process per opened Terminal, never in the consumer's own process.

```python
from logic.interface import MT5, Entity

print(Entity.Service.Currency().count())  # 8
print(MT5.Constants.TIMEFRAME_H1)  # 16385
```

## Interface

`logic.interface` is the only module that publishes. Under Interface contract version `1.1` it publishes one name per Service and nothing else:

| Name | What it is |
|---|---|
| `Entity` | The Entity Service Interface itself: one Child Service per Entity, the Entities they bind, and Database's Value, Instance, and Error groups. |
| `MT5` | The MT5 Service Interface itself: the Function Groups `Connection`, `Symbols`, `MarketBook`, `MarketData`, `Orders`, `Positions`, and `History`, which together hold every Function of the MetaTrader 5 package, the package's `Constants`, and `MT5Error`. |

## Services

- **Entity** (`Entity`): [README](logic/services/entity/README.md), [Definition](../.interface/implementation/development/logic/services/entity/entity.md), [Preferences](../.interface/implementation/development/logic/services/entity/entity.yaml).
- **MT5** (`MT5`): [README](logic/services/mt5/README.md), [Definition](../.interface/implementation/development/logic/services/mt5/mt5.md), [Preferences](../.interface/implementation/development/logic/services/mt5/mt5.yaml).

## Setup

Logic uses Python 3.14 or newer and `uv`, and depends on the Entity and Database Components beside it in this repository. From this directory:

```sh
uv sync
```

This creates `.venv` with Logic, the Entity library from `../entity`, and the Database library from `../database` as an editable dependency, so that Database keeps using its own Configuration and storage. On Windows it also installs the `MetaTrader5` package, which MT5 Service needs together with an installed MetaTrader 5 terminal on the same machine; the package exists only for Windows, so elsewhere Logic installs without it and only MT5 Service's Terminals cannot be opened. Prepare Database's default Instance once before use, from `../database`:

```sh
uv run python scripts/prepare.py
```

Another Component of this repository depends on Logic through a local path dependency in its own `pyproject.toml`:

```toml
[project]
dependencies = ["logic"]

[tool.uv.sources]
logic = { path = "../logic" }
database = { path = "../database", editable = true }
```

## Use

Import from Logic Interface only, and select a Service by its name:

```python
from logic.interface import Entity

currencies = Entity.Service.Currency()
usd = currencies.list(
    filters=[
        Entity.database_value.Filter(
            Entity.Entity.Currency.code,
            Entity.database_value.FilterOperator.EQUALS,
            "USD",
        )
    ]
)
print(usd[0].symbol)  # $
```

MT5 Service needs Windows, the `MetaTrader5` package, and a running MetaTrader 5 terminal; every call goes to the Function Group that holds its Function, names the terminal it works with, and takes and returns JSON values, every date and time as a Timestamp in seconds:

```python
from logic.interface import MT5

TERMINAL = r"C:\Program Files\MetaTrader 5\terminal64.exe"
MT5.Connection.initialize(TERMINAL, TERMINAL)  # True
print(MT5.Symbols.symbol_info_tick(TERMINAL, "EURUSD")["bid"])
H1 = MT5.Constants.TIMEFRAME_H1
print(MT5.MarketData.copy_rates_from(TERMINAL, "EURUSD", H1, 1790812800, 10))
MT5.Connection.shutdown(TERMINAL)
```

## Verify

From this directory:

```sh
uv sync --locked
uv run ruff format --check .
uv run ruff check .
uv run ty check
```

Then check in a fresh interpreter that Logic Interface publishes exactly every listed Service, each as its own Interface:

```python
import logic.interface as interface
from logic.services.entity import interface as entity_service
from logic.services.mt5 import interface as mt5_service

assert sorted(interface.__all__) == ["Entity", "MT5"]
assert interface.Entity is entity_service
assert interface.MT5 is mt5_service
print("verified")
```

## Troubleshooting

- **`database_error.ConfigurationError` saying `config.yaml` is missing**: Database was installed as a copy instead of from `../database`. Keep `database = { path = "../database", editable = true }` in the consumer's `[tool.uv.sources]` and run `uv sync` again.
- **`database_error.ExecutionError` with `no such table`**: Database's default Instance has not been prepared. Run `uv run python scripts/prepare.py` in `../database`.
- **`database_error.InvalidInputError` saying `Expected an instance of ...`**: an Entity instance was given to another Entity's Child Service. Use the Child Service of the same name, such as `Entity.Service.Broker()` for `Entity.Entity.Broker`.
- **`MT5Error` with code `-10003`, `The MetaTrader5 package cannot be loaded`**: the package is not installed, which is always the case off Windows. Run Logic on Windows and `uv sync` there.
- **`MT5Error` with code `-10004`, `This Terminal has no running Terminal Process`**: the Terminal was not opened, its opening failed, it was shut down, or the process that opened it has ended. Call `MT5.Connection.initialize` with that terminal first.
- **`MT5Error` with code `-2`, `... is not a JSON value` or `... is not a Timestamp`**: a parameter was given as a Python object such as a `datetime`, `Decimal`, tuple, or bytes. Pass JSON values only, and every date and time as whole seconds since 1970-01-01 00:00:00 UTC.
- **A script that opens a Terminal starts itself again**: Terminal Processes are started with `spawn`. Put the script's own code under `if __name__ == "__main__":`.
- **A change in Entity or Database does not show up**: the Entity library is installed as a copy; run `uv sync` again after it changes.
