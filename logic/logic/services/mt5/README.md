# MT5 Service

## Overview

MT5 Service is the Logic Service that performs every function of the official MetaTrader 5 Python package, [`MetaTrader5`](https://www.mql5.com/en/docs/python_metatrader5), on a MetaTrader 5 terminal chosen by name. It is the only part of the application that uses the package, so every other part — including the API — works with MetaTrader 5 through it and exchanges only JSON values.

```python
from logic.services.mt5.interface import MT5

demo = MT5("demo")
demo.Connection.initialize()
print(demo.Connection.terminal_info())
demo.Connection.shutdown()
```

## Interface

The MT5 Service Interface publishes one name, the `MT5` class, and nothing else. The class itself carries the constants, `MT5.Constants`, and the error, `MT5.Error`, so everything of MT5 Service is reached through `MT5`.

Create an MT5 instance with the name of a Terminal in `config.yaml`: `MT5("demo")`. An unknown name raises `MT5.Error`; creating an instance opens no connection. Every instance exposes the seven Function Groups below under their own names, and every call through it goes to its Terminal. Any number of instances may exist at once, for different Terminals or for the same one.

Every method takes exactly the parameters of its package function, with the same names, order, and defaults, and nothing else. A named optional parameter left as `None` is not sent, so the package applies its own default. Every date and time is a Timestamp — whole seconds since 1970-01-01 UTC. Every result is a JSON value, with a number that is not finite (NaN or infinity) returned as `null`, and every failure raises `MT5.Error`.

The examples below use `demo = MT5("demo")`.

### Connection

| Function | Example |
|---|---|
| `initialize` | `demo.Connection.initialize(login=25115284, password="...", server="MetaQuotes-Demo")` |
| `login` | `demo.Connection.login(25115284, password="...", server="MetaQuotes-Demo")` |
| `shutdown` | `demo.Connection.shutdown()` |
| `version` | `demo.Connection.version()` → `[500, 2007, 1551052800]`, the release date 25 Feb 2019 as a Timestamp |
| `last_error` | `demo.Connection.last_error()` → `[1, "Success"]` |
| `account_info` | `demo.Connection.account_info()["balance"]` |
| `terminal_info` | `demo.Connection.terminal_info()["connected"]` |

`initialize` starts the Terminal's own process and connects through the `path` configured for it; passing a different `path` is refused.

### Symbols

| Function | Example |
|---|---|
| `symbols_total` | `demo.Symbols.symbols_total()` |
| `symbols_get` | `demo.Symbols.symbols_get(group="*USD*")` |
| `symbol_info` | `demo.Symbols.symbol_info("EURUSD")["spread"]` |
| `symbol_info_tick` | `demo.Symbols.symbol_info_tick("EURUSD")["bid"]` |
| `symbol_select` | `demo.Symbols.symbol_select("EURUSD", True)` |

### MarketBook

| Function | Example |
|---|---|
| `market_book_add` | `demo.MarketBook.market_book_add("EURUSD")` |
| `market_book_get` | `demo.MarketBook.market_book_get("EURUSD")` |
| `market_book_release` | `demo.MarketBook.market_book_release("EURUSD")` |

### MarketData

| Function | Example |
|---|---|
| `copy_rates_from` | `demo.MarketData.copy_rates_from("EURUSD", h1, 1704067200, 10)` |
| `copy_rates_from_pos` | `demo.MarketData.copy_rates_from_pos("EURUSD", h1, 0, 10)` |
| `copy_rates_range` | `demo.MarketData.copy_rates_range("EURUSD", h1, 1704067200, 1704153600)` |
| `copy_ticks_from` | `demo.MarketData.copy_ticks_from("EURUSD", 1704067200, 100, all_ticks)` |
| `copy_ticks_range` | `demo.MarketData.copy_ticks_range("EURUSD", 1704067200, 1704070800, all_ticks)` |

Here `h1 = MT5.Constants.TIMEFRAME_H1` and `all_ticks = MT5.Constants.COPY_TICKS_ALL`. Bars and ticks are returned as a list of objects keyed by the package's column names, such as `time`, `open`, and `close`.

### Orders

| Function | Example |
|---|---|
| `orders_total` | `demo.Orders.orders_total()` |
| `orders_get` | `demo.Orders.orders_get(symbol="EURUSD")` |
| `order_calc_margin` | `demo.Orders.order_calc_margin(buy, "EURUSD", 1.0, 1.0850)` |
| `order_calc_profit` | `demo.Orders.order_calc_profit(buy, "EURUSD", 1.0, 1.0850, 1.0900)` |
| `order_check` | `demo.Orders.order_check(request)["retcode"]` |
| `order_send` | `demo.Orders.order_send(request)["order"]` |

Here `buy = MT5.Constants.ORDER_TYPE_BUY`, and `request` is a trade request object such as `{"action": MT5.Constants.TRADE_ACTION_DEAL, "symbol": "EURUSD", "volume": 0.1, "type": buy, "price": 1.0850}`.

### Positions

| Function | Example |
|---|---|
| `positions_total` | `demo.Positions.positions_total()` |
| `positions_get` | `demo.Positions.positions_get(symbol="EURUSD")` |

### History

| Function | Example |
|---|---|
| `history_orders_total` | `demo.History.history_orders_total(1704067200, 1706745600)` |
| `history_orders_get` | `demo.History.history_orders_get(1704067200, 1706745600, group="*USD*")` |
| `history_deals_total` | `demo.History.history_deals_total(1704067200, 1706745600)` |
| `history_deals_get` | `demo.History.history_deals_get(position=530218319)` |

### Constants

`MT5.Constants` holds every constant of the package by its own name. It is read on the class itself, without creating an MT5 instance, and through any instance as well. Read one value as an attribute, or all of them as a dictionary from name to value, and pass the value to a function:

```python
from logic.services.mt5.interface import MT5

MT5.Constants.TIMEFRAME_H1  # 16385
MT5.Constants.all()  # {"TIMEFRAME_H1": 16385, "ORDER_TYPE_BUY": 0, ...}
```

Every constant is written out in MT5 Service with the name and value the package (`MetaTrader5` 5.0.6231) gives it, so reading the Constants needs neither the package nor a terminal.

### MT5.Error

`MT5.Error` is raised for every failure; catch it with `except MT5.Error`. Its `code` and `message` are those of the package's `last_error` when the package reports the failure. Otherwise MT5 Service uses the package's own error codes: `RES_E_INVALID_PARAMS` (`-2`) for invalid input, such as an unknown Terminal name, a Terminal without a `path`, an invalid `config.yaml`, or a parameter that is not a JSON value; `RES_E_INTERNAL_FAIL_TIMEOUT` (`-10005`) for a call not answered within `call_timeout`; and `RES_E_FAIL` (`-1`) for its other failures, such as a call to a Terminal that is not initialized or a call where the package is not installed. An error message never contains a password or an API key.

## Use

1. Add each Terminal to `config.yaml`, next to this file, under the `terminals` section, keyed by its unique name, with the `path` of its terminal executable. The file comes with a sample Terminal named `demo` whose fields are empty; fill in its `path`, or add a Terminal of your own:

   ```yaml
   general:
     call_timeout: 60

   terminals:
     demo:
       path: ""
       username: ""
       password: ""
       investor_password: ""
       ip: ""
       port:
       api_key: ""
       description: ""
     live:
       path: C:\Program Files\MetaTrader 5\terminal64.exe
       username: ""
       password: ""
       investor_password: ""
       ip: ""
       port:
       api_key: ""
       description: My live terminal
   ```

   Every Terminal lists all of these fields. `username`, `password`, `investor_password`, `ip`, `api_key`, and `description` are strings and `port` is an integer; all of them may be left empty. `username`, `password`, `investor_password`, `ip`, `port`, and `api_key` are only stored, as plain text, and are not used by MT5 Service for now. The `general` section holds `call_timeout`, the number of seconds a call waits for its Terminal to answer; a call not answered in time raises `MT5.Error` and ends that Terminal's process, so it must be initialized again. Any other section or field, a missing field, a repeated name, or a value of the wrong type makes creating an MT5 instance and every call fail with `MT5.Error` (`-2`) naming each problem. A Terminal whose `path` is empty is refused when a call goes to it. The file is read once and read again only when it changes, so an edit takes effect without a restart.

2. Create an MT5 instance for each Terminal you use and call its Functions:

   ```python
   from logic.services.mt5.interface import MT5

   live = MT5("live")
   try:
       bars = live.MarketData.copy_rates_from_pos(
           "EURUSD", MT5.Constants.TIMEFRAME_H1, 0, 10
       )
   except MT5.Error as error:
       print(error.code, error.message)
   ```

Each Terminal runs in its own process: calls for one Terminal run one after another, also when they come from several MT5 instances of that Terminal, and calls for different Terminals run at the same time. Starting one Terminal never holds back calls for another. When the program ends normally, every running Terminal is shut down. Use MT5 Service from only one process of a program: a server that runs several worker processes uses it from only one of them, so each Terminal has one process. Where the package is not installed, MT5 Service still installs and loads, and every call to a Terminal raises `MT5.Error`.

## Verify

Compare the Function Groups with the [package documentation](https://www.mql5.com/en/docs/python_metatrader5):

- every function in the documentation's function list appears exactly once in the Interface tables above, under its group, and each group of an MT5 instance has exactly those methods;
- each method's parameters match the function's documented call signature in name, order, and default;
- `MT5.Constants.all()` holds exactly the constants the package defines, with the same names and values, on any machine;
- on a Windows machine with MetaTrader 5 installed and a Terminal in `config.yaml`, `MT5("<name>").Connection.terminal_info()` returns that Terminal's data once its Terminal Process is running.
