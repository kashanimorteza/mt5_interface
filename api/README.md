# API

## Overview

API is the project's one running network boundary. It serves every Group beneath its own segment of one Base URL, has no Endpoint of its own, and reaches the application only through Logic Interface; today it serves Entity Group, which turns every Entity Service Action into an Endpoint. From this directory:

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

The MT5 Group named by the Target is reserved and not yet defined, so API does not serve it yet.

## Setup

API uses Python 3.14 or newer and `uv`. It depends on the Logic library beside it, which brings the Database and Entity libraries. From this directory:

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

A client sends each request to the Base URL, then the Group segment, then the Adapter segment and the Endpoint path, with a JSON Body for `POST`, `PUT`, and `PATCH`. Every error comes back as Problem Details (`application/problem+json`). The [Entity Group documentation](api/groups/entity/README.md) lists every Endpoint with its Method, Path, and Parameters.

```sh
curl -s -X POST "$BASE/entity/asset/count" -H 'content-type: application/json' \
  -d '{"filters": [{"field": "category", "operator": "EQUALS", "value": "Commodity"}]}'
# 2
```

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
assert segments == {"entity"}
assert [group["name"] for group in description["x-tagGroups"]] == ["Entity"]
print("verified")
```

## Troubleshooting

- **Every request answers `404`**: the request is missing the URL Key or the Group segment. Build requests from `url` in `config.yaml`, then add `/entity/<adapter>/<endpoint>`.
- **`500` with `type` `ExecutionError` and `no such table`**: Database's default Instance has not been prepared. Run `uv run python scripts/prepare.py` in `../database`.
- **`500` with `type` `ConfigurationError` saying `config.yaml` is missing**: Database was installed as a copy. Run `uv sync` in this directory so the Logic library brings Database from `../database` again.
- **`422` with `type` `RequestValidationError`**: the request Body is not JSON of the stated shape, for example a Parameter that is not nested under its own name.
- **API does not start because the port is in use**: another process listens on the configured `port`. Stop it, or change `port` in `config.yaml` together with `url` and `documentation`.
