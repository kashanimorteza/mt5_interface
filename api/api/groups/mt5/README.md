# MT5 Group

## Overview

MT5 Group is the API Group that serves MT5 Service over HTTP: one Adapter for every Function Group of MT5 Service, one Endpoint for every Function of that group, and one Constants Endpoint. Every Function Endpoint takes the Function's own parameters plus `terminal`, the name of a Terminal in MT5 Service's `config.yaml`; its Handler creates an MT5 instance for that Terminal through Logic Interface, calls the same Function, and returns the result unchanged.

```bash
curl -X POST "<url>/MT5/symbols/symbol_info" \
  -H "Content-Type: application/json" \
  -d '{"terminal": "demo", "symbol": "EURUSD"}'
```

`<url>` is the Base URL in the API's `config.yaml`.

## Endpoints

Every Endpoint is `POST <url>/MT5/<adapter>/<function>` and takes its Parameters as one JSON object in the request body. Every Function Endpoint requires `terminal`; every other Parameter keeps the Function's name, requirement, and default, and an omitted optional Parameter keeps the Function's default. Every date and time is a Timestamp — whole seconds since 1970-01-01 UTC. A result is the Function's JSON value; an error is Problem Details (`application/problem+json`) whose `type` is the error's class, such as `MT5Error`.

### Connection

| Method | Path | Parameters | Example body |
|---|---|---|---|
| `POST` | `/MT5/connection/initialize` | `terminal`, `path` = null, `login` = null, `password` = null, `server` = null, `timeout` = null, `portable` = false | `{"terminal": "demo", "login": 25115284, "password": "...", "server": "MetaQuotes-Demo"}` |
| `POST` | `/MT5/connection/login` | `terminal`, `login`, `password` = null, `server` = null, `timeout` = null | `{"terminal": "demo", "login": 25115284, "password": "...", "server": "MetaQuotes-Demo"}` |
| `POST` | `/MT5/connection/shutdown` | `terminal` | `{"terminal": "demo"}` |
| `POST` | `/MT5/connection/version` | `terminal` | `{"terminal": "demo"}` |
| `POST` | `/MT5/connection/last_error` | `terminal` | `{"terminal": "demo"}` |
| `POST` | `/MT5/connection/account_info` | `terminal` | `{"terminal": "demo"}` |
| `POST` | `/MT5/connection/terminal_info` | `terminal` | `{"terminal": "demo"}` |

### Symbols

| Method | Path | Parameters | Example body |
|---|---|---|---|
| `POST` | `/MT5/symbols/symbols_total` | `terminal` | `{"terminal": "demo"}` |
| `POST` | `/MT5/symbols/symbols_get` | `terminal`, `group` = null | `{"terminal": "demo", "group": "*USD*"}` |
| `POST` | `/MT5/symbols/symbol_info` | `terminal`, `symbol` | `{"terminal": "demo", "symbol": "EURUSD"}` |
| `POST` | `/MT5/symbols/symbol_info_tick` | `terminal`, `symbol` | `{"terminal": "demo", "symbol": "EURUSD"}` |
| `POST` | `/MT5/symbols/symbol_select` | `terminal`, `symbol`, `enable` = null | `{"terminal": "demo", "symbol": "EURUSD", "enable": true}` |

### MarketBook

| Method | Path | Parameters | Example body |
|---|---|---|---|
| `POST` | `/MT5/market_book/market_book_add` | `terminal`, `symbol` | `{"terminal": "demo", "symbol": "EURUSD"}` |
| `POST` | `/MT5/market_book/market_book_get` | `terminal`, `symbol` | `{"terminal": "demo", "symbol": "EURUSD"}` |
| `POST` | `/MT5/market_book/market_book_release` | `terminal`, `symbol` | `{"terminal": "demo", "symbol": "EURUSD"}` |

### MarketData

| Method | Path | Parameters | Example body |
|---|---|---|---|
| `POST` | `/MT5/market_data/copy_rates_from` | `terminal`, `symbol`, `timeframe`, `date_from`, `count` | `{"terminal": "demo", "symbol": "EURUSD", "timeframe": 16385, "date_from": 1704067200, "count": 10}` |
| `POST` | `/MT5/market_data/copy_rates_from_pos` | `terminal`, `symbol`, `timeframe`, `start_pos`, `count` | `{"terminal": "demo", "symbol": "EURUSD", "timeframe": 16385, "start_pos": 0, "count": 10}` |
| `POST` | `/MT5/market_data/copy_rates_range` | `terminal`, `symbol`, `timeframe`, `date_from`, `date_to` | `{"terminal": "demo", "symbol": "EURUSD", "timeframe": 16385, "date_from": 1704067200, "date_to": 1704153600}` |
| `POST` | `/MT5/market_data/copy_ticks_from` | `terminal`, `symbol`, `date_from`, `count`, `flags` | `{"terminal": "demo", "symbol": "EURUSD", "date_from": 1704067200, "count": 100, "flags": -1}` |
| `POST` | `/MT5/market_data/copy_ticks_range` | `terminal`, `symbol`, `date_from`, `date_to`, `flags` | `{"terminal": "demo", "symbol": "EURUSD", "date_from": 1704067200, "date_to": 1704070800, "flags": -1}` |

`timeframe` and `flags` take a Constant's value, such as `16385` for `TIMEFRAME_H1` and `-1` for `COPY_TICKS_ALL`.

### Orders

| Method | Path | Parameters | Example body |
|---|---|---|---|
| `POST` | `/MT5/orders/orders_total` | `terminal` | `{"terminal": "demo"}` |
| `POST` | `/MT5/orders/orders_get` | `terminal`, `symbol` = null, `group` = null, `ticket` = null | `{"terminal": "demo", "symbol": "EURUSD"}` |
| `POST` | `/MT5/orders/order_calc_margin` | `terminal`, `action`, `symbol`, `volume`, `price` | `{"terminal": "demo", "action": 0, "symbol": "EURUSD", "volume": 0.1, "price": 1.1}` |
| `POST` | `/MT5/orders/order_calc_profit` | `terminal`, `action`, `symbol`, `volume`, `price_open`, `price_close` | `{"terminal": "demo", "action": 0, "symbol": "EURUSD", "volume": 0.1, "price_open": 1.1, "price_close": 1.11}` |
| `POST` | `/MT5/orders/order_check` | `terminal`, `request` | `{"terminal": "demo", "request": {"action": 1, "symbol": "EURUSD", "volume": 0.1, "type": 0, "price": 1.1}}` |
| `POST` | `/MT5/orders/order_send` | `terminal`, `request` | `{"terminal": "demo", "request": {"action": 1, "symbol": "EURUSD", "volume": 0.1, "type": 0, "price": 1.1}}` |

`request` is the trade request as a JSON object of its fields, with Constant values such as `1` for `TRADE_ACTION_DEAL` and `0` for `ORDER_TYPE_BUY`.

### Positions

| Method | Path | Parameters | Example body |
|---|---|---|---|
| `POST` | `/MT5/positions/positions_total` | `terminal` | `{"terminal": "demo"}` |
| `POST` | `/MT5/positions/positions_get` | `terminal`, `symbol` = null, `group` = null, `ticket` = null | `{"terminal": "demo", "group": "*USD*"}` |

### History

| Method | Path | Parameters | Example body |
|---|---|---|---|
| `POST` | `/MT5/history/history_orders_total` | `terminal`, `date_from`, `date_to` | `{"terminal": "demo", "date_from": 1704067200, "date_to": 1706745600}` |
| `POST` | `/MT5/history/history_orders_get` | `terminal`, `date_from` = null, `date_to` = null, `group` = null, `ticket` = null, `position` = null | `{"terminal": "demo", "date_from": 1704067200, "date_to": 1706745600, "group": "*USD*"}` |
| `POST` | `/MT5/history/history_deals_total` | `terminal`, `date_from`, `date_to` | `{"terminal": "demo", "date_from": 1704067200, "date_to": 1706745600}` |
| `POST` | `/MT5/history/history_deals_get` | `terminal`, `date_from` = null, `date_to` = null, `group` = null, `ticket` = null, `position` = null | `{"terminal": "demo", "position": 530218319}` |

### Constants

| Method | Path | Parameters | Example body |
|---|---|---|---|
| `POST` | `/MT5/constants/all` | none | `{}` |

Returns every Constant of MT5 Service as one JSON object from name to value, such as `"TIMEFRAME_H1": 16385`. It needs no Terminal and works where the MetaTrader 5 package is not installed.

## Use

1. Add the Terminal to MT5 Service's `config.yaml` under its name with the `path` of its terminal executable; the sample `demo` Terminal shows the fields.
2. Start the session: `POST <url>/MT5/connection/initialize` with `{"terminal": "<name>"}` and, when needed, the account's `login`, `password`, and `server`.
3. Call any other Endpoint with the same `terminal` and the Function's Parameters, reading Constant values from `POST <url>/MT5/constants/all` where a Parameter needs one.
4. End the session: `POST <url>/MT5/connection/shutdown` with `{"terminal": "<name>"}`.

Every request is independent: the Endpoint creates an MT5 instance for the named Terminal on each call, and MT5 Service keeps the Terminal's process between calls inside each API worker process; see the API documentation's Troubleshooting when `workers` is above 1. A failure, such as a Terminal name that is not in `config.yaml` or a call before `initialize`, returns Problem Details with `type` `MT5Error` and the code and message MT5 Service raised in `detail`.

## Verify

Open the interactive documentation at `<url>/docs` (or `<url>/redoc`). The `MT5` group holds one section per Adapter — `MT5 · Connection`, `MT5 · Symbols`, `MT5 · MarketBook`, `MT5 · MarketData`, `MT5 · Orders`, `MT5 · Positions`, `MT5 · History`, and `MT5 · Constants` — and each Function Group's section lists exactly one Endpoint per Function of that group in MT5 Service, 32 in all, plus the one Constants Endpoint. Compare each section with the Function Group table in the MT5 Service documentation: every Function appears once, under its own name, with the same Parameters plus `terminal`.
