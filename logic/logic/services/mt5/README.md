# MT5 Service

## Overview

MT5 Service is the one part of the application that uses the official MetaTrader 5 Python package, `MetaTrader5`. It offers every Function of the package with the same name, parameters, and defaults, plus one more parameter, `terminal`, the path of the MetaTrader 5 terminal the call works with, in seven Function Groups, each a class of its own. Each Terminal runs in its own Terminal Process, so several Terminals work at the same time. Every parameter is a JSON value, every result is a JSON value (objects, arrays, strings, numbers, booleans, and `null`), every date and time is a Timestamp (whole seconds since 1970-01-01 00:00:00 UTC), and every failure the package reports is raised as `MT5Error`:

```python
from logic.services.mt5.interface import Connection

TERMINAL = r"C:\Program Files\MetaTrader 5\terminal64.exe"
Connection.initialize(TERMINAL, TERMINAL)  # True: the Terminal Process starts
print(Connection.terminal_info(TERMINAL)["connected"])  # True
Connection.shutdown(TERMINAL)  # the Terminal Process ends
```

Inside Logic, reach it as `MT5` through Logic Interface: `from logic.interface import MT5`, then `MT5.Connection`, `MT5.MarketData`, and so on.

## Interface

`logic.services.mt5.interface` publishes exactly 9 names, under Interface contract version `1.0`, and nothing else: the Function Groups `Connection`, `Symbols`, `MarketBook`, `MarketData`, `Orders`, `Positions`, `History`, then `Constants` and `MT5Error`. Loading it opens no connection to MetaTrader 5 and starts no Terminal Process; the package itself is never published.

### Function Groups

MT5 Service names its Function Groups itself, and every Function of the package documentation belongs to exactly one of them: `Connection` (7), `Symbols` (5), `MarketBook` (3), `MarketData` (5), `Orders` (6), `Positions` (2), `History` (4). Each is a class in its own unit that can be imported on its own, with one method for every Function of its group. Every method is static, takes `terminal` first, and then exactly its Function's parameters; a parameter left as `None` is not sent, so the package applies its own default, except an unnamed one left out before a later unnamed one that is given, which is sent as `None`.

#### Connection

| Function | Parameters | Action |
|---|---|---|
| `initialize` | `(terminal: str, path: str | None = None, *, login: int | None = None, password: str | None = None, server: str | None = None, timeout: int | None = None, portable: bool = False)` | Establish a connection with the MetaTrader 5 terminal. |
| `login` | `(terminal: str, login: int, *, password: str | None = None, server: str | None = None, timeout: int | None = None)` | Connect to a trading account using specified parameters. |
| `shutdown` | `(terminal: str)` | Close the previously established connection to the MetaTrader 5 terminal. |
| `version` | `(terminal: str)` | Return the MetaTrader 5 terminal version. |
| `last_error` | `(terminal: str)` | Return data on the last error. |
| `account_info` | `(terminal: str)` | Get info on the current trading account. |
| `terminal_info` | `(terminal: str)` | Get the connected MetaTrader 5 client terminal status and settings. |

#### Symbols

| Function | Parameters | Action |
|---|---|---|
| `symbols_total` | `(terminal: str)` | Get the number of all financial instruments in the MetaTrader 5 terminal. |
| `symbols_get` | `(terminal: str, group: str | None = None)` | Get all financial instruments from the MetaTrader 5 terminal. |
| `symbol_info` | `(terminal: str, symbol: str)` | Get data on the specified financial instrument. |
| `symbol_info_tick` | `(terminal: str, symbol: str)` | Get the last tick for the specified financial instrument. |
| `symbol_select` | `(terminal: str, symbol: str, enable: bool | None = None)` | Select a symbol in the MarketWatch window or remove a symbol from the window. |

#### MarketBook

| Function | Parameters | Action |
|---|---|---|
| `market_book_add` | `(terminal: str, symbol: str)` | Subscribes the MetaTrader 5 terminal to the Market Depth change events for a specified symbol. |
| `market_book_get` | `(terminal: str, symbol: str)` | Returns a tuple from BookInfo featuring Market Depth entries for the specified symbol. |
| `market_book_release` | `(terminal: str, symbol: str)` | Cancels subscription of the MetaTrader 5 terminal to the Market Depth change events for a specified symbol. |

#### MarketData

| Function | Parameters | Action |
|---|---|---|
| `copy_rates_from` | `(terminal: str, symbol: str, timeframe: int, date_from: int, count: int)` | Get bars from the MetaTrader 5 terminal starting from the specified date. |
| `copy_rates_from_pos` | `(terminal: str, symbol: str, timeframe: int, start_pos: int, count: int)` | Get bars from the MetaTrader 5 terminal starting from the specified index. |
| `copy_rates_range` | `(terminal: str, symbol: str, timeframe: int, date_from: int, date_to: int)` | Get bars in the specified date range from the MetaTrader 5 terminal. |
| `copy_ticks_from` | `(terminal: str, symbol: str, date_from: int, count: int, flags: int)` | Get ticks from the MetaTrader 5 terminal starting from the specified date. |
| `copy_ticks_range` | `(terminal: str, symbol: str, date_from: int, date_to: int, flags: int)` | Get ticks for the specified date range from the MetaTrader 5 terminal. |

#### Orders

| Function | Parameters | Action |
|---|---|---|
| `orders_total` | `(terminal: str)` | Get the number of active orders. |
| `orders_get` | `(terminal: str, *, symbol: str | None = None, group: str | None = None, ticket: int | None = None)` | Get active orders with the ability to filter by symbol or ticket. |
| `order_calc_margin` | `(terminal: str, action: int, symbol: str, volume: float, price: float)` | Return margin in the account currency to perform a specified trading operation. |
| `order_calc_profit` | `(terminal: str, action: int, symbol: str, volume: float, price_open: float, price_close: float)` | Return profit in the account currency for a specified trading operation. |
| `order_check` | `(terminal: str, request: dict[str, typing.Any])` | Check funds sufficiency for performing a required trading operation. Check result are returned as the MqlTradeCheckResult structure. |
| `order_send` | `(terminal: str, request: dict[str, typing.Any])` | Send a request to perform a trading operation from the terminal to the trade server. The function is similar to OrderSend. |

#### Positions

| Function | Parameters | Action |
|---|---|---|
| `positions_total` | `(terminal: str)` | Get the number of open positions. |
| `positions_get` | `(terminal: str, *, symbol: str | None = None, group: str | None = None, ticket: int | None = None)` | Get open positions with the ability to filter by symbol or ticket. |

#### History

| Function | Parameters | Action |
|---|---|---|
| `history_orders_total` | `(terminal: str, date_from: int, date_to: int)` | Get the number of orders in trading history within the specified interval. |
| `history_orders_get` | `(terminal: str, date_from: int | None = None, date_to: int | None = None, *, group: str | None = None, ticket: int | None = None, position: int | None = None)` | Get orders from trading history with the ability to filter by ticket or position. |
| `history_deals_total` | `(terminal: str, date_from: int, date_to: int)` | Get the number of deals in trading history within the specified interval. |
| `history_deals_get` | `(terminal: str, date_from: int | None = None, date_to: int | None = None, *, group: str | None = None, ticket: int | None = None, position: int | None = None)` | Get deals from trading history within the specified interval with the ability to filter by ticket or position. |

`initialize` starts the Terminal Process of a Terminal that has none and opens the Terminal in it; if that first opening fails, the process ends again. `shutdown` closes the Terminal and ends its process, and the process also ends when the process that opened the Terminal ends. Every other call runs in the Terminal Process of the Terminal it names, one after another for one Terminal; a call for a Terminal with no running process raises `MT5Error` with code `-10004`.

### JSON parameters and results

Every parameter, `terminal` included, is a JSON value: a string, number, boolean, `None`, list, or dictionary with string keys made of such values. `date_from` and `date_to` are Timestamps, passed to the package as they are; a whole-number float such as `1788220800.0` is taken as `1788220800`. Any other value, such as a `datetime`, a `Decimal`, a tuple, or bytes, is refused with `MT5Error` code `-2` before anything reaches the package. Results keep the package's field names and values: a named tuple becomes a dictionary, an array of bars or ticks becomes a list of dictionaries keyed by its columns, and a tuple becomes a list. Dates and times in results are Timestamps as the package gives them, such as `time`, `time_setup`, and `time_update`; the `*_msc` fields are the package's own millisecond counts.

One example for each Function, given an open Terminal:

```python
from logic.services.mt5.interface import (
    Connection,
    Constants,
    History,
    MarketBook,
    MarketData,
    Orders,
    Positions,
    Symbols,
)

T = r"C:\Program Files\MetaTrader 5\terminal64.exe"
PASSWORD, SERVER = "<password>", "<server>"
START = 1788220800  # 2026-09-01 00:00:00 UTC
END = 1790812800  # 2026-10-01 00:00:00 UTC
H1 = Constants.TIMEFRAME_H1
BUY = Constants.ORDER_TYPE_BUY
REQUEST = {
    "action": Constants.TRADE_ACTION_DEAL,
    "symbol": "EURUSD",
    "volume": 0.1,
    "type": BUY,
    "price": Symbols.symbol_info_tick(T, "EURUSD")["ask"],
    "type_filling": Constants.ORDER_FILLING_IOC,
}

Connection.initialize(T, T, login=12345678, password=PASSWORD, server=SERVER)
Connection.login(T, 12345678, password=PASSWORD, server=SERVER)  # True
Connection.shutdown(T)  # True; the Terminal Process ends
Connection.version(T)  # [500, <build>, '<release date>']
Connection.last_error(T)  # [1, 'Success']
Connection.account_info(T)["balance"]
Connection.terminal_info(T)["connected"]  # True
Symbols.symbols_total(T)
Symbols.symbols_get(T, group="*USD*")  # a list of symbol dictionaries
Symbols.symbol_info(T, "EURUSD")["digits"]
Symbols.symbol_info_tick(T, "EURUSD")["time"]  # a Timestamp
Symbols.symbol_select(T, "EURUSD", True)  # True
MarketBook.market_book_add(T, "EURUSD")  # True
MarketBook.market_book_get(T, "EURUSD")  # [{type, price, volume, ...}]
MarketBook.market_book_release(T, "EURUSD")  # True
MarketData.copy_rates_from(T, "EURUSD", H1, START, 10)
MarketData.copy_rates_from_pos(T, "EURUSD", H1, 0, 10)
MarketData.copy_rates_range(T, "EURUSD", H1, START, END)
MarketData.copy_ticks_from(T, "EURUSD", START, 100, Constants.COPY_TICKS_ALL)
MarketData.copy_ticks_range(T, "EURUSD", START, END, Constants.COPY_TICKS_INFO)
Orders.orders_total(T)
Orders.orders_get(T, symbol="EURUSD")
Orders.order_calc_margin(T, BUY, "EURUSD", 0.1, 1.1)
Orders.order_calc_profit(T, BUY, "EURUSD", 0.1, 1.1, 1.11)
Orders.order_check(T, REQUEST)["retcode"]
Orders.order_send(T, REQUEST)["retcode"]  # TRADE_RETCODE_DONE if executed
Positions.positions_total(T)
Positions.positions_get(T, group="*EUR*")
History.history_orders_total(T, START, END)
History.history_orders_get(T, position=123456789)
History.history_deals_total(T, START, END)
History.history_deals_get(T, START, END, group="EUR*")
```

### Constants

`Constants` holds every one of the package's 223 named constants under its own name with its own value, read from the package's source when MT5 Service was generated: `TIMEFRAME_*` (21), `COPY_TICKS_*` (3), `TICK_FLAG_*` (6), `POSITION_*` (6), `ORDER_*` (34), `DEAL_*` (32), `TRADE_ACTION_*` (6), `TRADE_RETCODE_*` (40), `SYMBOL_*` (41), `DAY_OF_WEEK_*` (7), `ACCOUNT_*` (8), `BOOK_TYPE_*` (4), `RES_*` (15). Pass a Constant's value to a Function unchanged; `Constants.get()` returns all of them as a dictionary from name to value, without a Terminal:

```python
from logic.services.mt5.interface import Constants

print(Constants.TIMEFRAME_H1)  # 16385
print(Constants.get()["ORDER_TYPE_SELL"])  # 1
print(len(Constants.get()))  # 223
```

### MT5Error

The one error every method raises when the package reports a failure (its documented failure value, `None` or `False`), with the `code` and `message` the package's `last_error` gives for that Terminal. Code `-2` from the package's own table also reports a parameter that is not a JSON value, and codes `-10002` to `-10005` a Terminal Process that ended mid-call, could not load the package, could not be reached, or did not start in time:

```python
from logic.services.mt5.interface import MarketData, MT5Error

CLOSED = r"C:\MetaTrader 5 (not opened)\terminal64.exe"
try:
    MarketData.copy_rates_from_pos(CLOSED, "EURUSD", 16385, 0, 10)
except MT5Error as error:
    print(error.code)  # -10004
    print(error.message)  # This Terminal has no running Terminal Process; open it first
```

## Use

1. Import the Function Groups you need, and the Constants when a Function takes one, such as `from logic.services.mt5.interface import Connection, Constants, MarketData`.
2. Open each Terminal once with `Connection.initialize`, passing its path as `terminal`; send connection details such as `login`, `password`, and `server` through `initialize` or `login`.
3. Call any Function on its Function Group with that `terminal` and the Function's own parameters as JSON values, every date and time as a Timestamp; read a dictionary or list back, and catch `MT5Error` for failures.
4. Close the Terminal with `Connection.shutdown` when it is no longer needed.

The package runs only on Windows, next to an installed MetaTrader 5 terminal. Elsewhere the package is not installed, and opening a Terminal raises `MT5Error` with code `-10003`. Terminal Processes are started with `spawn`, so a script that opens a Terminal guards its own code with `if __name__ == "__main__":`. Processes started by the same parent share its authentication key, so they all reach the same Terminal Process; a process started by a parent that does not share that key cannot reach it.

## Verify

That the Function Groups together have one method per Function of the [package documentation](https://www.mql5.com/en/docs/python_metatrader5), each in exactly one group with its exact name, and that `Constants` matches the package. Run this on Windows with the package installed:

```python
import inspect

import MetaTrader5

from logic.services.mt5.interface import (
    Connection,
    Constants,
    History,
    MarketBook,
    MarketData,
    Orders,
    Positions,
    Symbols,
)

groups = [Connection, Symbols, MarketBook, MarketData, Orders, Positions, History]
methods = [n for g in groups for n, v in vars(g).items() if isinstance(v, staticmethod)]
print(len(methods), len(set(methods)))  # 32 32
print(all(callable(getattr(MetaTrader5, n)) for n in methods))  # True
signatures = [
    inspect.signature(getattr(g, n)) for g in groups for n in vars(g) if n in methods
]
print({next(iter(s.parameters)) for s in signatures})  # {'terminal'}
values = vars(MetaTrader5).items()
package = {n: v for n, v in values if n.isupper() and type(v) is int}
print(Constants.get() == package)  # True
```
