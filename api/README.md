# API

## Overview

API is the project's one running network boundary. It serves every Group beneath its own segment of one Base URL, has no Endpoint of its own, and reaches the application only through Logic Interface; it serves Entity Group, which turns every Entity Service Action into an Endpoint, and MT5 Group, which turns every MT5 Service Function, and so every MetaTrader 5 Function, into an Endpoint. From this directory:

```sh
BASE=$(uv run python -c "import yaml; print(yaml.safe_load(open('config.yaml'))['url'])")
curl -s "$BASE/entity/currency/get_by_id/1"
# {"id": 1, "user_id": 1, "code": "USD", "symbol": "$", "country": "United States", "decimal_digits": 2, "is_active": true, "description": null}
```

## Configuration

API reads every runtime value from `config.yaml` in this directory, and from nowhere else:

| Value | Meaning |
|---|---|
| `title` | The title the running API and its interactive documentation present. |
| `description` | The description they present; may be empty. |
| `key` | The URL Key: an opaque, random path segment placed before every Group segment. It was generated once and is kept; it only changes the address and does not authenticate a request. Keep it out of shared documents. |
| `host` | The address API binds to. |
| `port` | The port API binds to. |
| `workers` | The number of worker processes. |
| `transport_protocol` | The protocol used to form the URL. |
| `url` | The Base URL: `<transport_protocol>://<host>:<port>/<key>`, written in lower-case scheme, such as `http://127.0.0.1:8000/<key>`. With an empty key it has no key segment. |
| `documentation` | The addresses of the interactive documentation: `<url>/docs` (Swagger UI) and `<url>/redoc` (ReDoc). |

Every Endpoint is served at `<url>/<group segment>/<adapter segment><endpoint path>`.

## Groups

| Group | Segment | Documentation |
|---|---|---|
| Entity | `entity` | [Entity Group](api/groups/entity/README.md) |
| MT5 | `mt5` | [MT5 Group](api/groups/mt5/README.md) |

## Setup

API uses Python 3.14 or newer and `uv`. It depends on the Logic library beside it, which brings the Database and Entity libraries and, on Windows, the `MetaTrader5` package. MT5 Group's Endpoints work only where that package runs: on Windows, next to an installed MetaTrader 5 terminal. Elsewhere API still installs and serves every Endpoint, and opening a Terminal answers `MT5Error`. From this directory:

```sh
uv sync
```

Prepare Database's default Instance once, in `../database`:

```sh
(cd ../database && uv run python scripts/prepare.py > /dev/null)
```

Then start API; it binds to the configured host and port with the configured workers, and runs until stopped:

```text
uv run api
```

## Use

A client sends each request to the Base URL, then the Group segment, then the Adapter segment and the Endpoint path, with a JSON Body for `POST`, `PUT`, and `PATCH`. Every error comes back as Problem Details (`application/problem+json`). The [Entity Group documentation](api/groups/entity/README.md) and the [MT5 Group documentation](api/groups/mt5/README.md) list every Endpoint with its Method, Path, and Parameters.

```sh
curl -s -X POST "$BASE/entity/asset/count" -H 'content-type: application/json' \
  -d '{"filters": [{"field": "category", "operator": "EQUALS", "value": "Commodity"}]}'
# 2
curl -s "$BASE/mt5/constants/get" | python3 -c "import json, sys; print(json.load(sys.stdin)['TIMEFRAME_H1'])"
# 16385
```

Every MT5 Group Function Endpoint names its MetaTrader 5 terminal in `terminal`; open it once with `initialize` before calling other Functions for it, and close it with `shutdown`. A Terminal opened through one request is used by every later request naming it, whichever worker serves the request.

The interactive documentation lists every Endpoint, one section per Adapter gathered under its Group, at the `documentation` addresses in `config.yaml`.

## Verify

From this directory:

```text
uv sync --locked
uv run ruff format --check .
uv run ruff check .
uv run ty check
```

Then, with API running, check that every listed Group is served beneath its segment and nothing else is:

```python
import json
import urllib.request

import yaml

base = yaml.safe_load(open("config.yaml"))["url"]
description = json.load(urllib.request.urlopen(f"{base}/openapi.json"))
prefix = base.split("://", 1)[1].split("/", 1)[1]
segments = {path.split("/")[2] for path in description["paths"]}
assert all(path.startswith(f"/{prefix}/") for path in description["paths"])
assert segments == {"entity", "mt5"}
assert [group["name"] for group in description["x-tagGroups"]] == ["Entity", "MT5"]
print("verified")
```

## Troubleshooting

- **Every request answers `404`**: the request is missing the URL Key or the Group segment. Build requests from `url` in `config.yaml`, then add `/entity/<adapter>/<endpoint>`.
- **`500` with `type` `ExecutionError` and `no such table`**: Database's default Instance has not been prepared. Run `uv run python scripts/prepare.py` in `../database`.
- **`500` with `type` `ConfigurationError` saying `config.yaml` is missing**: Database was installed as a copy. Run `uv sync` in this directory so the Logic library brings Database from `../database` again.
- **`422` with `type` `RequestValidationError`**: the request Body is not JSON of the stated shape, for example a Parameter that is not nested under its own name.
- **`500` with `type` `MT5Error` and detail `-10003: The MetaTrader5 package cannot be loaded`**: API runs where the `MetaTrader5` package is not installed, which is always the case off Windows. Run API on Windows and `uv sync` there.
- **`500` with `type` `MT5Error` and detail `-10004: This Terminal has no running Terminal Process`**: the Terminal named in `terminal` is not open, its opening failed, it was shut down, or the API worker that opened it has stopped (also when API restarts). Call `/mt5/python_integration/initialize` with it first.
- **`500` with `type` `MT5Error` and another code**: the MetaTrader 5 package reported a failure; the detail holds its `last_error` code and message.
- **API does not start because the port is in use**: another process listens on the configured `port`. Stop it, or change `port` in `config.yaml` together with `url` and `documentation`.
