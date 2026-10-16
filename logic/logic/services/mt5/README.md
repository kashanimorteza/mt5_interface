# MT5 Service

## Overview

MT5 Service is the Logic Service that performs every function of the official MetaTrader 5 Python package, [`MetaTrader5`](https://www.mql5.com/en/docs/python_metatrader5), on a MetaTrader 5 terminal chosen by name. It is the only part of the application that uses the package, so every other part — including the API — works with MetaTrader 5 through it and exchanges only JSON values.

```python
from logic.services.mt5.interface import Connection

Connection.initialize("demo")
print(Connection.terminal_info("demo"))
Connection.shutdown("demo")
```

## Interface

The MT5 Service Interface publishes the seven Function Groups, `Constants`, and `MT5Error`, and nothing else. Every method takes the parameters of its package function, with the same names, order, and defaults, plus `terminal` first: the `name` of a Terminal declared in `config.yaml`. A named optional parameter left as `None` is not sent, so the package applies its own default. Every date and time is a Timestamp — whole seconds since 1970-01-01 UTC. Every result is a JSON value, and every failure raises `MT5Error`.

### Connection

| Function | Example |
|---|---|
| `initialize` | `Connection.initialize("demo", login=25115284, password="...", server="MetaQuotes-Demo")` |
| `login` | `Connection.login("demo", 25115284, password="...", server="MetaQuotes-Demo")` |
| `shutdown` | `Connection.shutdown("demo")` |
| `version` | `Connection.version("demo")` → `[500, 2007, 1551052800]`, the release date 25 Feb 2019 as a Timestamp |
| `last_error` | `Connection.last_error("demo")` → `[1, "Success"]` |
| `account_info` | `Connection.account_info("demo")["balance"]` |
| `terminal_info` | `Connection.terminal_info("demo")["connected"]` |

`initialize` starts the Terminal's own process and connects through the `path` configured for it; passing a different `path` is refused.

### Symbols

| Function | Example |
|---|---|
| `symbols_total` | `Symbols.symbols_total("demo")` |
| `symbols_get` | `Symbols.symbols_get("demo", group="*USD*")` |
| `symbol_info` | `Symbols.symbol_info("demo", "EURUSD")["spread"]` |
| `symbol_info_tick` | `Symbols.symbol_info_tick("demo", "EURUSD")["bid"]` |
| `symbol_select` | `Symbols.symbol_select("demo", "EURUSD", True)` |

### MarketBook

| Function | Example |
|---|---|
| `market_book_add` | `MarketBook.market_book_add("demo", "EURUSD")` |
| `market_book_get` | `MarketBook.market_book_get("demo", "EURUSD")` |
| `market_book_release` | `MarketBook.market_book_release("demo", "EURUSD")` |

### MarketData

| Function | Example |
|---|---|
| `copy_rates_from` | `MarketData.copy_rates_from("demo", "EURUSD", h1, 1704067200, 10)` |
| `copy_rates_from_pos` | `MarketData.copy_rates_from_pos("demo", "EURUSD", h1, 0, 10)` |
| `copy_rates_range` | `MarketData.copy_rates_range("demo", "EURUSD", h1, 1704067200, 1704153600)` |
| `copy_ticks_from` | `MarketData.copy_ticks_from("demo", "EURUSD", 1704067200, 100, all_ticks)` |
| `copy_ticks_range` | `MarketData.copy_ticks_range("demo", "EURUSD", 1704067200, 1704070800, all_ticks)` |

Here `h1 = Constants.TIMEFRAME_H1` and `all_ticks = Constants.COPY_TICKS_ALL`. Bars and ticks are returned as a list of objects keyed by the package's column names, such as `time`, `open`, and `close`.

### Orders

| Function | Example |
|---|---|
| `orders_total` | `Orders.orders_total("demo")` |
| `orders_get` | `Orders.orders_get("demo", symbol="EURUSD")` |
| `order_calc_margin` | `Orders.order_calc_margin("demo", buy, "EURUSD", 1.0, 1.0850)` |
| `order_calc_profit` | `Orders.order_calc_profit("demo", buy, "EURUSD", 1.0, 1.0850, 1.0900)` |
| `order_check` | `Orders.order_check("demo", request)["retcode"]` |
| `order_send` | `Orders.order_send("demo", request)["order"]` |

Here `buy = Constants.ORDER_TYPE_BUY`, and `request` is a trade request object such as `{"action": Constants.TRADE_ACTION_DEAL, "symbol": "EURUSD", "volume": 0.1, "type": buy, "price": 1.0850}`.

### Positions

| Function | Example |
|---|---|
| `positions_total` | `Positions.positions_total("demo")` |
| `positions_get` | `Positions.positions_get("demo", symbol="EURUSD")` |

### History

| Function | Example |
|---|---|
| `history_orders_total` | `History.history_orders_total("demo", 1704067200, 1706745600)` |
| `history_orders_get` | `History.history_orders_get("demo", 1704067200, 1706745600, group="*USD*")` |
| `history_deals_total` | `History.history_deals_total("demo", 1704067200, 1706745600)` |
| `history_deals_get` | `History.history_deals_get("demo", position=530218319)` |

### Constants

`Constants` holds every constant of the package by its own name. Read one value as an attribute, or all of them as a dictionary from name to value, and pass the value to a function:

```python
from logic.services.mt5.interface import Constants

Constants.TIMEFRAME_H1  # 16385
Constants.all()  # {"TIMEFRAME_H1": 16385, "ORDER_TYPE_BUY": 0, ...}
```

Every constant is written out in MT5 Service with the name and value the package (`MetaTrader5` 5.0.6231) gives it, so reading the Constants needs neither the package nor a terminal.

### MT5Error

`MT5Error` is raised for every failure. Its `code` and `message` are those of the package's `last_error` when the package reports the failure; MT5 Service uses `-2` for invalid input, such as an unknown Terminal name, a Terminal without a `path`, an invalid `config.yaml`, or a parameter that is not a JSON value, and `-1` for its other failures, such as a call to a Terminal that is not initialized.

## Use

1. Add each Terminal to `config.yaml`, next to this file, as one entry of its `terminals` section with a unique `name` and the `path` of its terminal executable. The file comes with a sample entry named `demo` whose fields are empty; fill in its `path`, or add an entry of your own:

   ```yaml
   general: {}

   terminals:
     - name: demo
       path: C:\Program Files\MetaTrader 5\terminal64.exe
       description: MetaQuotes demo account
   ```

   An entry may also hold `username`, `password`, `investor_password`, `ip`, `api_key` (strings), and `port` (an integer). These are only stored, as plain text, may be left empty, and are not used by MT5 Service for now. Keep the `general` section; it has no settings yet. Any other field or section, a missing `name` or `path`, a repeated `name`, or a value of the wrong type makes every call fail with `MT5Error` (`-2`) listing each problem. A Terminal whose `path` is empty is refused when a call names it. The file is read on every call, so an edit takes effect without a restart.

2. Import the Function Groups you need from the MT5 Service Interface and initialize the Terminal before any other call:

   ```python
   from logic.services.mt5.interface import Constants, Connection, MarketData, MT5Error

   Connection.initialize("demo")
   try:
       bars = MarketData.copy_rates_from_pos(
           "demo", "EURUSD", Constants.TIMEFRAME_H1, 0, 10
       )
   except MT5Error as error:
       print(error.code, error.message)
   finally:
       Connection.shutdown("demo")
   ```

Each Terminal runs in its own process: calls for one Terminal run one after another, and calls for different Terminals run at the same time.

## Verify

Compare the Function Groups with the [package documentation](https://www.mql5.com/en/docs/python_metatrader5):

- every function in the documentation's function list appears exactly once in the Interface tables above, under its group, and each group's class has exactly those methods;
- each method's parameters after `terminal` match the function's documented call signature in name, order, and default;
- `Constants.all()` holds exactly the constants the package defines, with the same names and values, on any machine;
- on a Windows machine with MetaTrader 5 installed and a Terminal in `config.yaml`, `Connection.initialize` followed by `Connection.terminal_info` returns that Terminal's data.
