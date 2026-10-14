# MT5 Group

## Overview

MT5 Group serves MT5 Service over HTTP beneath the Group segment `mt5`: one Adapter for every Function Group of MT5 Service, holding one Endpoint for every Function, and one Adapter for the Constants. Every Handler calls its Function through Logic Interface and returns its result unchanged, so an external program can use every MetaTrader 5 Function without the MetaTrader 5 package. Every Function Endpoint takes `terminal`, the path of the MetaTrader 5 terminal it works with. The examples use `BASE`, the Base URL from API's `config.yaml`, read in the API Component directory, and `TERMINAL`, a terminal path on the Windows machine that runs API:

```sh
BASE=$(uv run python -c "import yaml; print(yaml.safe_load(open('config.yaml'))['url'])")
TERMINAL='C:\\Program Files\\MetaTrader 5\\terminal64.exe'
curl -s -X POST "$BASE/mt5/python_integration/initialize" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "path": "'"$TERMINAL"'"}'
# true
```

## Endpoints

### `python_integration`: Python Integration Function Group

One Endpoint for every Function, in the package documentation's order. Every Endpoint is `POST`, because no Function's name begins with a verb in API's verb table, and takes its Parameters as one JSON object in Body; a Parameter left out takes its default, and an optional Parameter left out is not sent to the package.

| Method | Path | Parameters |
|---|---|---|
| `POST` | `/mt5/python_integration/initialize` | `terminal`, `path` (optional), `login` (optional), `password` (optional), `server` (optional), `timeout` (optional), `portable` (default `false`) |
| `POST` | `/mt5/python_integration/login` | `terminal`, `login`, `password` (optional), `server` (optional), `timeout` (optional) |
| `POST` | `/mt5/python_integration/shutdown` | `terminal` |
| `POST` | `/mt5/python_integration/version` | `terminal` |
| `POST` | `/mt5/python_integration/last_error` | `terminal` |
| `POST` | `/mt5/python_integration/account_info` | `terminal` |
| `POST` | `/mt5/python_integration/terminal_info` | `terminal` |
| `POST` | `/mt5/python_integration/symbols_total` | `terminal` |
| `POST` | `/mt5/python_integration/symbols_get` | `terminal`, `group` (optional) |
| `POST` | `/mt5/python_integration/symbol_info` | `terminal`, `symbol` |
| `POST` | `/mt5/python_integration/symbol_info_tick` | `terminal`, `symbol` |
| `POST` | `/mt5/python_integration/symbol_select` | `terminal`, `symbol`, `enable` (optional) |
| `POST` | `/mt5/python_integration/market_book_add` | `terminal`, `symbol` |
| `POST` | `/mt5/python_integration/market_book_get` | `terminal`, `symbol` |
| `POST` | `/mt5/python_integration/market_book_release` | `terminal`, `symbol` |
| `POST` | `/mt5/python_integration/copy_rates_from` | `terminal`, `symbol`, `timeframe`, `date_from`, `count` |
| `POST` | `/mt5/python_integration/copy_rates_from_pos` | `terminal`, `symbol`, `timeframe`, `start_pos`, `count` |
| `POST` | `/mt5/python_integration/copy_rates_range` | `terminal`, `symbol`, `timeframe`, `date_from`, `date_to` |
| `POST` | `/mt5/python_integration/copy_ticks_from` | `terminal`, `symbol`, `date_from`, `count`, `flags` |
| `POST` | `/mt5/python_integration/copy_ticks_range` | `terminal`, `symbol`, `date_from`, `date_to`, `flags` |
| `POST` | `/mt5/python_integration/orders_total` | `terminal` |
| `POST` | `/mt5/python_integration/orders_get` | `terminal`, `symbol` (optional), `group` (optional), `ticket` (optional) |
| `POST` | `/mt5/python_integration/order_calc_margin` | `terminal`, `action`, `symbol`, `volume`, `price` |
| `POST` | `/mt5/python_integration/order_calc_profit` | `terminal`, `action`, `symbol`, `volume`, `price_open`, `price_close` |
| `POST` | `/mt5/python_integration/order_check` | `terminal`, `request` |
| `POST` | `/mt5/python_integration/order_send` | `terminal`, `request` |
| `POST` | `/mt5/python_integration/positions_total` | `terminal` |
| `POST` | `/mt5/python_integration/positions_get` | `terminal`, `symbol` (optional), `group` (optional), `ticket` (optional) |
| `POST` | `/mt5/python_integration/history_orders_total` | `terminal`, `date_from`, `date_to` |
| `POST` | `/mt5/python_integration/history_orders_get` | `terminal`, `date_from` (optional), `date_to` (optional), `group` (optional), `ticket` (optional), `position` (optional) |
| `POST` | `/mt5/python_integration/history_deals_total` | `terminal`, `date_from`, `date_to` |
| `POST` | `/mt5/python_integration/history_deals_get` | `terminal`, `date_from` (optional), `date_to` (optional), `group` (optional), `ticket` (optional), `position` (optional) |

```sh
curl -s -X POST "$BASE/mt5/python_integration/initialize" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "path": "'"$TERMINAL"'"}'
# true
curl -s -X POST "$BASE/mt5/python_integration/login" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "login": 12345678}'
# true
curl -s -X POST "$BASE/mt5/python_integration/shutdown" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'"}'
# null
curl -s -X POST "$BASE/mt5/python_integration/version" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'"}'
# [500, <build>, "<release date>"]
curl -s -X POST "$BASE/mt5/python_integration/last_error" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'"}'
# [1, "Success"]
curl -s -X POST "$BASE/mt5/python_integration/account_info" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'"}'
# {"login": 12345678, "balance": ..., ...}
curl -s -X POST "$BASE/mt5/python_integration/terminal_info" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'"}'
# {"connected": true, ...}
curl -s -X POST "$BASE/mt5/python_integration/symbols_total" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'"}'
# <number of symbols>
curl -s -X POST "$BASE/mt5/python_integration/symbols_get" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "group": "*USD*"}'
# [...]
curl -s -X POST "$BASE/mt5/python_integration/symbol_info" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD"}'
# {...}
curl -s -X POST "$BASE/mt5/python_integration/symbol_info_tick" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD"}'
# {...}
curl -s -X POST "$BASE/mt5/python_integration/symbol_select" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD", "enable": true}'
# true
curl -s -X POST "$BASE/mt5/python_integration/market_book_add" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD"}'
# true
curl -s -X POST "$BASE/mt5/python_integration/market_book_get" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD"}'
# [...]
curl -s -X POST "$BASE/mt5/python_integration/market_book_release" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD"}'
# true
curl -s -X POST "$BASE/mt5/python_integration/copy_rates_from" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD", "timeframe": 16385, "date_from": "2026-09-01T00:00:00Z", "count": 10}'
# [{"time": ..., "open": ..., "high": ..., "low": ..., "close": ..., ...}]
curl -s -X POST "$BASE/mt5/python_integration/copy_rates_from_pos" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD", "timeframe": 16385, "start_pos": 0, "count": 10}'
# [...]
curl -s -X POST "$BASE/mt5/python_integration/copy_rates_range" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD", "timeframe": 16385, "date_from": "2026-09-01T00:00:00Z", "date_to": "2026-10-01T00:00:00Z"}'
# [...]
curl -s -X POST "$BASE/mt5/python_integration/copy_ticks_from" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD", "date_from": "2026-09-01T00:00:00Z", "count": 10, "flags": -1}'
# [{"time": ..., "bid": ..., "ask": ..., ...}]
curl -s -X POST "$BASE/mt5/python_integration/copy_ticks_range" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD", "date_from": "2026-09-01T00:00:00Z", "date_to": "2026-10-01T00:00:00Z", "flags": -1}'
# [...]
curl -s -X POST "$BASE/mt5/python_integration/orders_total" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'"}'
# <number of orders>
curl -s -X POST "$BASE/mt5/python_integration/orders_get" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "symbol": "EURUSD"}'
# [...]
curl -s -X POST "$BASE/mt5/python_integration/order_calc_margin" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "action": 0, "symbol": "EURUSD", "volume": 0.1, "price": 1.1}'
# <margin>
curl -s -X POST "$BASE/mt5/python_integration/order_calc_profit" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "action": 0, "symbol": "EURUSD", "volume": 0.1, "price_open": 1.1, "price_close": 1.11}'
# <profit>
curl -s -X POST "$BASE/mt5/python_integration/order_check" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "request": {"action": 1, "symbol": "EURUSD", "volume": 0.1, "type": 0, "price": 1.1, "type_filling": 1}}'
# {"retcode": 0, "request": {...}, ...}
curl -s -X POST "$BASE/mt5/python_integration/order_send" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "request": {"action": 1, "symbol": "EURUSD", "volume": 0.1, "type": 0, "price": 1.1, "type_filling": 1}}'
# {"retcode": 10009, "request": {...}, ...}
curl -s -X POST "$BASE/mt5/python_integration/positions_total" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'"}'
# <number of positions>
curl -s -X POST "$BASE/mt5/python_integration/positions_get" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "group": "*USD*"}'
# [...]
curl -s -X POST "$BASE/mt5/python_integration/history_orders_total" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "date_from": "2026-09-01T00:00:00Z", "date_to": "2026-10-01T00:00:00Z"}'
# <number of orders>
curl -s -X POST "$BASE/mt5/python_integration/history_orders_get" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "position": 123456789}'
# [...]
curl -s -X POST "$BASE/mt5/python_integration/history_deals_total" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "date_from": "2026-09-01T00:00:00Z", "date_to": "2026-10-01T00:00:00Z"}'
# <number of deals>
curl -s -X POST "$BASE/mt5/python_integration/history_deals_get" -H 'content-type: application/json' -d '{"terminal": "'"$TERMINAL"'", "date_from": "2026-09-01T00:00:00Z", "date_to": "2026-10-01T00:00:00Z", "group": "*USD*"}'
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

Results are MT5 Service's Plain Data: a named tuple arrives as an object with the package's field names, bars and ticks as a list of objects keyed by their columns, and a tuple as a list. Dates travel as ISO 8601 text or as seconds since 1970-01-01; a Constant's value, never its name, is sent where a Function takes one.

## Use

1. Read the Constants once from `GET $BASE/mt5/constants/get` to find the values Functions take, such as `TIMEFRAME_H1` or `ORDER_TYPE_BUY`.
2. Open each Terminal with `initialize`, sending its path as `terminal`, and the account through `initialize` or `login`.
3. Call any Function Endpoint with the same `terminal` and the Function's Parameters as one JSON object.
4. Close the Terminal with `shutdown` when it is no longer needed.

A failure the package reports is answered as RFC 9457 Problem Details with status `500`, `type` `MT5Error`, and `detail` `<code>: <message>` from the package's `last_error`; a Terminal that is not open answers code `-10004`, and a request missing a required Parameter answers `422`:

```sh
curl -s -X POST "$BASE/mt5/python_integration/account_info" -H 'content-type: application/json' -d '{"terminal": "C:\\not-opened\\terminal64.exe"}'
# {"type":"MT5Error","title":"MT5Error","status":500,"detail":"-10004: This Terminal has no running Terminal Process; open it first"}
```

## Verify

That every Function of MT5 Service has exactly one Endpoint and the Constants one more. From the API Component directory:

```sh
uv run python - <<'EOF'
import api.bootstrap as bootstrap
from logic.interface import MT5

functions = [n for n, v in vars(MT5.PythonIntegration).items() if isinstance(v, staticmethod)]
paths = [p.split("/mt5/", 1)[1] for p in bootstrap.app.openapi()["paths"] if "/mt5/" in p]
print(paths == [f"python_integration/{n}" for n in functions] + ["constants/get"])
EOF
# True
```
