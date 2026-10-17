# API

## Overview

API is the executable of MT5 Interface: one REST boundary that serves every Group beneath its own URL segment and has no Endpoint of its own. Its only Group is MT5, through which external programs call every function of the MetaTrader 5 Python package on a Terminal they name, using MT5 Service of the Logic library.

```bash
curl -X POST "<url>/MT5/connection/terminal_info" \
  -H "Content-Type: application/json" \
  -d '{"terminal": "demo"}'
```

## Configuration

API reads every runtime value from `config.yaml` in this directory and from nowhere else:

| Value | Meaning |
|---|---|
| `title` | The title the running API presents in its documentation. |
| `description` | The description the running API presents; may be empty. |
| `key` | The URL Key: an opaque path segment placed before every Group segment; empty omits it. It was generated once and is kept; it changes only the address and is not authentication. |
| `host` | The host or IP address API binds to. |
| `port` | The port API binds to. |
| `workers` | The number of API worker processes; `1`, because MT5 Service keeps every Terminal in one process. |
| `transport_protocol` | The transport protocol of the address, `HTTP`. |
| `url` | The Base URL, formed as `<transport_protocol>://<host>:<port>/<key>`, written in lower case and without `/<key>` when `key` is empty. |
| `documentation` | The interactive documentation addresses, `<url>/docs` and `<url>/redoc`. |

When you change `transport_protocol`, `host`, `port`, or `key`, change `url` and `documentation` to match, then restart API.

## Groups

| Group | Served at | Documentation |
|---|---|---|
| MT5 | `<url>/MT5` | [MT5 Group](api/groups/mt5/README.md) |

## Setup

Install [uv](https://docs.astral.sh/uv/) and run, from this directory:

```bash
uv sync
uv run api
```

`uv sync` creates `.venv` with Python 3.14, FastAPI, and the Logic library from `../logic`; `uv run api` serves API at `url` with `workers` processes. API installs and starts on any operating system. Calling MetaTrader 5 needs Windows, where the MetaTrader 5 package is installed with Logic, and a MetaTrader 5 terminal declared in MT5 Service's `config.yaml` (`../logic/logic/services/mt5/config.yaml`).

## Use

A client reaches a Group at `<url>/<Group>` and an Endpoint at `<url>/<Group>/<adapter>/<operation>`. The machine-readable API description is served at `<url>/openapi.json` (OpenAPI 3.1). It holds an overview of the API, every Endpoint with a description and an example for each Parameter, a link to the official documentation of its MetaTrader 5 function, every error response as Problem Details, and stable operation names such as `mt5_market_data_copy_rates_from`, so a person or an agent can use the API, or generate a client for it, from that file alone. Every MT5 Endpoint is `POST` with its Parameters as one JSON object in the request body; see the [MT5 Group documentation](api/groups/mt5/README.md). Every error is Problem Details (`application/problem+json`) with `type` set to the error's class name; an error that carries a code, such as `MT5Error`, also has a separate integer `code` member, and its `detail` is the message alone: `RequestValidationError` with status `422` for a request that does not match the Endpoint's Parameters, and `MT5Error` for a failure MT5 Service reports, with status `422` for invalid input (code `-2`, such as an unknown Terminal), `504` for a Terminal that did not answer in time (code `-10005`), and `500` otherwise.

## Verify

Start API and open `<url>/docs` or `<url>/redoc`. The documentation holds exactly one Group, `MT5`, whose sections are its Adapters; every Endpoint path begins with `/<key>/MT5/`, and no other path is listed besides the documentation itself. A request to a path without the URL Key, or beneath any other segment, returns `404`.

## Troubleshooting

- **`404` for every request** — the path lacks the URL Key or uses a different one. Use `url` from `config.yaml` as the start of every address.
- **`422` `RequestValidationError`** — a required Parameter is missing, has the wrong type, or the body is not a JSON object. The `detail` lists each problem with its location.
- **`422` `MT5Error` "Terminal '…' is not in config.yaml"** — the `terminal` name is not declared in MT5 Service's `config.yaml`. Add it there under its name.
- **`422` `MT5Error` "Terminal '…' has no path in config.yaml"** — the Terminal is declared without the `path` of its terminal executable, as the sample `demo` Terminal is. Fill in `path`.
- **`500` `MT5Error` on every MetaTrader 5 call although the Terminal is configured** — the MetaTrader 5 package is not available on this host; it installs only on Windows.
- **`500` `MT5Error` "Terminal '…' is not initialized" after a successful `initialize`** — `workers` in `config.yaml` is above `1`, so a later request reached another worker process. Keep `workers` at `1`, because MT5 Service keeps every Terminal in one process.
- **`504` `MT5Error` "Terminal '…' did not answer … within N seconds"** — the Terminal did not answer within `call_timeout` of MT5 Service's `config.yaml`; its process was ended, so call `initialize` again.
- **API does not start: address already in use** — another process holds `port`. Stop it, or change `port`, `url`, and `documentation` in `config.yaml`.
