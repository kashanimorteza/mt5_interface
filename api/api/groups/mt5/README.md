# MT5 Group

## Overview

MT5 Group serves MT5 Service over HTTP beneath the Group segment `mt5`: one Adapter for every Function Group of MT5 Service, holding one Endpoint for every Function, and one Adapter for the Constants. Every Handler calls its Function through Logic Interface and returns its result unchanged, so an external program can use every MetaTrader 5 Function without the MetaTrader 5 package. Every Function Endpoint takes `terminal`, the path of the MetaTrader 5 terminal it works with. The examples use `BASE`, the Base URL from API's `config.yaml`, read in the API Component directory, and `TERMINAL`, a terminal path on the Windows machine that runs API:

```sh
BASE=$(uv run python -c "import yaml; print(yaml.safe_load(open('config.yaml'))['url'])")
TERMINAL='C:\\Program Files\\MetaTrader 5\\terminal64.exe'
curl -s -X POST "$BASE/mt5/connection/initialize" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "path": "'"$TERMINAL"'"}'
# true
```

## Endpoints

One Adapter for every Function Group of MT5 Service, in MT5 Service's order, each named from its Function Group, and the Constants Adapter. Every Function Endpoint is `POST`, because no Function's name begins with a verb in API's verb table, and takes its Parameters as one JSON object in Body; a Parameter left out takes its default, and an optional Parameter left out is not sent to the package. `date_from` and `date_to` are Timestamps: whole seconds since 1970-01-01 00:00:00 UTC.

### `connection`: Connection Function Group

One Endpoint for every Function MT5 Service lists under `Connection`, in that order.

| Method | Path | Parameters |
|---|---|---|
| `POST` | `/mt5/connection/initialize` | `terminal`, `path` (optional), `login` (optional), `password` (optional), `server` (optional), `timeout` (optional), `portable` (default `false`) |
| `POST` | `/mt5/connection/login` | `terminal`, `login`, `password` (optional), `server` (optional), `timeout` (optional) |
| `POST` | `/mt5/connection/shutdown` | `terminal` |
| `POST` | `/mt5/connection/version` | `terminal` |
| `POST` | `/mt5/connection/last_error` | `terminal` |
| `POST` | `/mt5/connection/account_info` | `terminal` |
| `POST` | `/mt5/connection/terminal_info` | `terminal` |

```sh
curl -s -X POST "$BASE/mt5/connection/initialize" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "path": "'"$TERMINAL"'"}'
# true
curl -s -X POST "$BASE/mt5/connection/login" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "login": 12345678}'
# true
curl -s -X POST "$BASE/mt5/connection/shutdown" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'"}'
# null
curl -s -X POST "$BASE/mt5/connection/version" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'"}'
# [500, <build>, "<release date>"]
curl -s -X POST "$BASE/mt5/connection/last_error" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'"}'
# [1, "Success"]
curl -s -X POST "$BASE/mt5/connection/account_info" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'"}'
# {"login": 12345678, "balance": ..., ...}
curl -s -X POST "$BASE/mt5/connection/terminal_info" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'"}'
# {"connected": true, ...}
```

### `symbols`: Symbols Function Group

One Endpoint for every Function MT5 Service lists under `Symbols`, in that order.

| Method | Path | Parameters |
|---|---|---|
| `POST` | `/mt5/symbols/symbols_total` | `terminal` |
| `POST` | `/mt5/symbols/symbols_get` | `terminal`, `group` (optional) |
| `POST` | `/mt5/symbols/symbol_info` | `terminal`, `symbol` |
| `POST` | `/mt5/symbols/symbol_info_tick` | `terminal`, `symbol` |
| `POST` | `/mt5/symbols/symbol_select` | `terminal`, `symbol`, `enable` (optional) |

```sh
curl -s -X POST "$BASE/mt5/symbols/symbols_total" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'"}'
# <number of symbols>
curl -s -X POST "$BASE/mt5/symbols/symbols_get" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "group": "*USD*"}'
# [...]
curl -s -X POST "$BASE/mt5/symbols/symbol_info" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD"}'
# {...}
curl -s -X POST "$BASE/mt5/symbols/symbol_info_tick" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD"}'
# {...}
curl -s -X POST "$BASE/mt5/symbols/symbol_select" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD", "enable": true}'
# true
```

### `market_book`: MarketBook Function Group

One Endpoint for every Function MT5 Service lists under `MarketBook`, in that order.

| Method | Path | Parameters |
|---|---|---|
| `POST` | `/mt5/market_book/market_book_add` | `terminal`, `symbol` |
| `POST` | `/mt5/market_book/market_book_get` | `terminal`, `symbol` |
| `POST` | `/mt5/market_book/market_book_release` | `terminal`, `symbol` |

```sh
curl -s -X POST "$BASE/mt5/market_book/market_book_add" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD"}'
# true
curl -s -X POST "$BASE/mt5/market_book/market_book_get" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD"}'
# [...]
curl -s -X POST "$BASE/mt5/market_book/market_book_release" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD"}'
# true
```

### `market_data`: MarketData Function Group

One Endpoint for every Function MT5 Service lists under `MarketData`, in that order.

| Method | Path | Parameters |
|---|---|---|
| `POST` | `/mt5/market_data/copy_rates_from` | `terminal`, `symbol`, `timeframe`, `date_from`, `count` |
| `POST` | `/mt5/market_data/copy_rates_from_pos` | `terminal`, `symbol`, `timeframe`, `start_pos`, `count` |
| `POST` | `/mt5/market_data/copy_rates_range` | `terminal`, `symbol`, `timeframe`, `date_from`, `date_to` |
| `POST` | `/mt5/market_data/copy_ticks_from` | `terminal`, `symbol`, `date_from`, `count`, `flags` |
| `POST` | `/mt5/market_data/copy_ticks_range` | `terminal`, `symbol`, `date_from`, `date_to`, `flags` |

```sh
curl -s -X POST "$BASE/mt5/market_data/copy_rates_from" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD", "timeframe": 16385, "date_from": 1788220800, "count": 10}'
# [{"time": ..., "open": ..., "high": ..., "low": ..., "close": ..., ...}]
curl -s -X POST "$BASE/mt5/market_data/copy_rates_from_pos" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD", "timeframe": 16385, "start_pos": 0, "count": 10}'
# [...]
curl -s -X POST "$BASE/mt5/market_data/copy_rates_range" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD", "timeframe": 16385, "date_from": 1788220800, "date_to": 1790812800}'
# [...]
curl -s -X POST "$BASE/mt5/market_data/copy_ticks_from" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD", "date_from": 1788220800, "count": 10, "flags": -1}'
# [{"time": ..., "bid": ..., "ask": ..., ...}]
curl -s -X POST "$BASE/mt5/market_data/copy_ticks_range" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD", "date_from": 1788220800, "date_to": 1790812800, "flags": -1}'
# [...]
```

### `orders`: Orders Function Group

One Endpoint for every Function MT5 Service lists under `Orders`, in that order.

| Method | Path | Parameters |
|---|---|---|
| `POST` | `/mt5/orders/orders_total` | `terminal` |
| `POST` | `/mt5/orders/orders_get` | `terminal`, `symbol` (optional), `group` (optional), `ticket` (optional) |
| `POST` | `/mt5/orders/order_calc_margin` | `terminal`, `action`, `symbol`, `volume`, `price` |
| `POST` | `/mt5/orders/order_calc_profit` | `terminal`, `action`, `symbol`, `volume`, `price_open`, `price_close` |
| `POST` | `/mt5/orders/order_check` | `terminal`, `request` |
| `POST` | `/mt5/orders/order_send` | `terminal`, `request` |

```sh
curl -s -X POST "$BASE/mt5/orders/orders_total" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'"}'
# <number of orders>
curl -s -X POST "$BASE/mt5/orders/orders_get" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD"}'
# [...]
curl -s -X POST "$BASE/mt5/orders/order_calc_margin" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "action": 0, "symbol": "EURUSD", "volume": 0.1, "price": 1.1}'
# <margin>
curl -s -X POST "$BASE/mt5/orders/order_calc_profit" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "action": 0, "symbol": "EURUSD", "volume": 0.1, "price_open": 1.1, "price_close": 1.11}'
# <profit>
curl -s -X POST "$BASE/mt5/orders/order_check" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "request": {"action": 1, "symbol": "EURUSD", "volume": 0.1, "type": 0, "price": 1.1, "type_filling": 1}}'
# {"retcode": 0, "request": {...}, ...}
curl -s -X POST "$BASE/mt5/orders/order_send" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "request": {"action": 1, "symbol": "EURUSD", "volume": 0.1, "type": 0, "price": 1.1, "type_filling": 1}}'
# {"retcode": 10009, "request": {...}, ...}
```

### `positions`: Positions Function Group

One Endpoint for every Function MT5 Service lists under `Positions`, in that order.

| Method | Path | Parameters |
|---|---|---|
| `POST` | `/mt5/positions/positions_total` | `terminal` |
| `POST` | `/mt5/positions/positions_get` | `terminal`, `symbol` (optional), `group` (optional), `ticket` (optional) |

```sh
curl -s -X POST "$BASE/mt5/positions/positions_total" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'"}'
# <number of positions>
curl -s -X POST "$BASE/mt5/positions/positions_get" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "group": "*USD*"}'
# [...]
```

### `history`: History Function Group

One Endpoint for every Function MT5 Service lists under `History`, in that order.

| Method | Path | Parameters |
|---|---|---|
| `POST` | `/mt5/history/history_orders_total` | `terminal`, `date_from`, `date_to` |
| `POST` | `/mt5/history/history_orders_get` | `terminal`, `date_from` (optional), `date_to` (optional), `group` (optional), `ticket` (optional), `position` (optional) |
| `POST` | `/mt5/history/history_deals_total` | `terminal`, `date_from`, `date_to` |
| `POST` | `/mt5/history/history_deals_get` | `terminal`, `date_from` (optional), `date_to` (optional), `group` (optional), `ticket` (optional), `position` (optional) |

```sh
curl -s -X POST "$BASE/mt5/history/history_orders_total" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "date_from": 1788220800, "date_to": 1790812800}'
# <number of orders>
curl -s -X POST "$BASE/mt5/history/history_orders_get" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "position": 123456789}'
# [...]
curl -s -X POST "$BASE/mt5/history/history_deals_total" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "date_from": 1788220800, "date_to": 1790812800}'
# <number of deals>
curl -s -X POST "$BASE/mt5/history/history_deals_get" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "date_from": 1788220800, "date_to": 1790812800, "group": "*USD*"}'
# [...]
```

### `constants`: Constants

One Endpoint returning every Constant of MT5 Service by name and value. It takes no `terminal` and needs no open Terminal.

| Method | Path | Parameters |
|---|---|---|
| `GET` | `/mt5/constants/get` | none |

```sh
curl -s "$BASE/mt5/constants/get"
# {"TIMEFRAME_M1": 1, ..., "TIMEFRAME_H1": 16385, ...}
```

Results are MT5 Service's Plain Data: a named tuple arrives as an object with the package's field names, bars and ticks as a list of objects keyed by their columns, and a tuple as a list. Every date and time, in a request or a result, is a Timestamp, such as a bar's `time`; the `*_msc` fields are the package's own millisecond counts. A date sent as text answers `422`; a Constant's value, never its name, is sent where a Function takes one.

## Use

1. Read the Constants once from `GET $BASE/mt5/constants/get` to find the values Functions take, such as `TIMEFRAME_H1` or `ORDER_TYPE_BUY`.
2. Open each Terminal with `initialize`, sending its path as `terminal`, and the account through `initialize` or `login`.
3. Call any Function Endpoint with the same `terminal` and the Function's Parameters as one JSON object.
4. Close the Terminal with `shutdown` when it is no longer needed.

A failure the package reports is answered as RFC 9457 Problem Details with status `500`, `type` `MT5Error`, and `detail` `<code>: <message>` from the package's `last_error`; a Terminal that is not open answers code `-10004`, and a request missing a required Parameter answers `422`:

```sh
curl -s -X POST "$BASE/mt5/connection/account_info" -H 'content-type: application/json' -d '{"terminal": "C:\\not-opened\\terminal64.exe"}'
# {"type":"MT5Error","title":"MT5Error","status":500,"detail":"-10004: This Terminal has no running Terminal Process; open it first"}
```

## Verify

That every Function of every MT5 Service Function Group has exactly one Endpoint and the Constants one more. From the API Component directory:

```sh
uv run python - <<'EOF'
import api.bootstrap as bootstrap
from logic.interface import MT5

groups = [MT5.Connection, MT5.Symbols, MT5.MarketBook, MT5.MarketData, MT5.Orders, MT5.Positions, MT5.History]
functions = [n for g in groups for n, v in vars(g).items() if isinstance(v, staticmethod)]
paths = [p.split("/mt5/", 1)[1] for p in bootstrap.app.openapi()["paths"] if "/mt5/" in p]
print(sorted(p.split("/")[1] for p in paths if not p.startswith("constants/")) == sorted(functions))
print(len(paths) == len(functions) + 1 and "constants/get" in paths)
EOF
# True
# True
```
