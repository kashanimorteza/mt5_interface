# MT5 Service

## Overview

MT5 Service is the Logic Service that performs every function of the official MetaTrader 5 Python package, [`MetaTrader5`](https://www.mql5.com/en/docs/python_metatrader5), on a MetaTrader 5 terminal chosen by name. It is the only part of the application that uses the package, so every other part — including the API — works with MetaTrader 5 through it and exchanges only JSON values.

```python
from logic.services.mt5.interface import Connection

Connection.initialize("Demo")
print(Connection.terminal_info("Demo"))
Connection.shutdown("Demo")
```

## Interface

The MT5 Service Interface publishes the seven Function Groups, `Constants`, and `MT5Error`, and nothing else. Every method takes the parameters of its package function, with the same names, order, and defaults, plus `terminal` first: the `name` of a Terminal listed in `terminal.config`. A named optional parameter left as `None` is not sent, so the package applies its own default. Every date and time is a Timestamp — whole seconds since 1970-01-01 UTC. Every result is a JSON value, and every failure raises `MT5Error`.

### Connection

| Function | Example |
|---|---|
| `initialize` | `Connection.initialize("Demo", login=25115284, password="...", server="MetaQuotes-Demo")` |
| `login` | `Connection.login("Demo", 25115284, password="...", server="MetaQuotes-Demo")` |
| `shutdown` | `Connection.shutdown("Demo")` |
| `version` | `Connection.version("Demo")` → `[500, 2007, 1551052800]`, the release date 25 Feb 2019 as a Timestamp |
| `last_error` | `Connection.last_error("Demo")` → `[1, "Success"]` |
| `account_info` | `Connection.account_info("Demo")["balance"]` |
| `terminal_info` | `Connection.terminal_info("Demo")["connected"]` |

`initialize` starts the Terminal's own process and connects through the `path` configured for it; passing a different `path` is refused.

### Symbols

| Function | Example |
|---|---|
| `symbols_total` | `Symbols.symbols_total("Demo")` |
| `symbols_get` | `Symbols.symbols_get("Demo", group="*USD*")` |
| `symbol_info` | `Symbols.symbol_info("Demo", "EURUSD")["spread"]` |
| `symbol_info_tick` | `Symbols.symbol_info_tick("Demo", "EURUSD")["bid"]` |
| `symbol_select` | `Symbols.symbol_select("Demo", "EURUSD", True)` |

### MarketBook

| Function | Example |
|---|---|
| `market_book_add` | `MarketBook.market_book_add("Demo", "EURUSD")` |
| `market_book_get` | `MarketBook.market_book_get("Demo", "EURUSD")` |
| `market_book_release` | `MarketBook.market_book_release("Demo", "EURUSD")` |

### MarketData

| Function | Example |
|---|---|
| `copy_rates_from` | `MarketData.copy_rates_from("Demo", "EURUSD", h1, 1704067200, 10)` |
| `copy_rates_from_pos` | `MarketData.copy_rates_from_pos("Demo", "EURUSD", h1, 0, 10)` |
| `copy_rates_range` | `MarketData.copy_rates_range("Demo", "EURUSD", h1, 1704067200, 1704153600)` |
| `copy_ticks_from` | `MarketData.copy_ticks_from("Demo", "EURUSD", 1704067200, 100, all_ticks)` |
| `copy_ticks_range` | `MarketData.copy_ticks_range("Demo", "EURUSD", 1704067200, 1704070800, all_ticks)` |

Here `h1 = Constants.TIMEFRAME_H1` and `all_ticks = Constants.COPY_TICKS_ALL`. Bars and ticks are returned as a list of objects keyed by the package's column names, such as `time`, `open`, and `close`.

### Orders

| Function | Example |
|---|---|
| `orders_total` | `Orders.orders_total("Demo")` |
| `orders_get` | `Orders.orders_get("Demo", symbol="EURUSD")` |
| `order_calc_margin` | `Orders.order_calc_margin("Demo", buy, "EURUSD", 1.0, 1.0850)` |
| `order_calc_profit` | `Orders.order_calc_profit("Demo", buy, "EURUSD", 1.0, 1.0850, 1.0900)` |
| `order_check` | `Orders.order_check("Demo", request)["retcode"]` |
| `order_send` | `Orders.order_send("Demo", request)["order"]` |

Here `buy = Constants.ORDER_TYPE_BUY`, and `request` is a trade request object such as `{"action": Constants.TRADE_ACTION_DEAL, "symbol": "EURUSD", "volume": 0.1, "type": buy, "price": 1.0850}`.

### Positions

| Function | Example |
|---|---|
| `positions_total` | `Positions.positions_total("Demo")` |
| `positions_get` | `Positions.positions_get("Demo", symbol="EURUSD")` |

### History

| Function | Example |
|---|---|
| `history_orders_total` | `History.history_orders_total("Demo", 1704067200, 1706745600)` |
| `history_orders_get` | `History.history_orders_get("Demo", 1704067200, 1706745600, group="*USD*")` |
| `history_deals_total` | `History.history_deals_total("Demo", 1704067200, 1706745600)` |
| `history_deals_get` | `History.history_deals_get("Demo", position=530218319)` |

### Constants

`Constants` holds every constant of the package by its own name. Read one value as an attribute, or all of them as a dictionary from name to value, and pass the value to a function:

```python
from logic.services.mt5.interface import Constants

Constants.TIMEFRAME_H1  # 16385
Constants.all()  # {"TIMEFRAME_H1": 16385, "ORDER_TYPE_BUY": 0, ...}
```

The values are read from the package in a separate process the first time they are needed.

### MT5Error

`MT5Error` is raised for every failure. Its `code` and `message` are those of the package's `last_error` when the package reports the failure; MT5 Service uses `-2` for invalid input, such as an unknown Terminal name or a parameter that is not a JSON value, and `-1` for its other failures, such as a call to a Terminal that is not initialized.

## Use

1. List each Terminal in `terminal.config`, next to this file, with a unique `name` and the `path` of its terminal executable:

   ```yaml
   - name: Demo
     path: C:\Program Files\MetaTrader 5\terminal64.exe
   ```

2. Import the Function Groups you need from the MT5 Service Interface and initialize the Terminal before any other call:

   ```python
   from logic.services.mt5.interface import Constants, Connection, MarketData, MT5Error

   Connection.initialize("Demo")
   try:
       bars = MarketData.copy_rates_from_pos(
           "Demo", "EURUSD", Constants.TIMEFRAME_H1, 0, 10
       )
   except MT5Error as error:
       print(error.code, error.message)
   finally:
       Connection.shutdown("Demo")
   ```

Each Terminal runs in its own process: calls for one Terminal run one after another, and calls for different Terminals run at the same time.

## Verify

Compare the Function Groups with the [package documentation](https://www.mql5.com/en/docs/python_metatrader5):

- every function in the documentation's function list appears exactly once in the Interface tables above, under its group, and each group's class has exactly those methods;
- each method's parameters after `terminal` match the function's documented call signature in name, order, and default;
- on a Windows machine with MetaTrader 5 installed, `Constants.all()` returns the package's constants and `Connection.initialize` followed by `Connection.terminal_info` returns the configured Terminal's data.
