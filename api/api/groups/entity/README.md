# Entity Group

## Overview

Entity Group serves Entity Service over HTTP: one Adapter for every Entity, beneath the Group segment `entity`, and in each Adapter one Endpoint for every Action of that Entity's Child Service. Every Handler calls its Action through Logic Interface and returns its result unchanged, so the Endpoints answer exactly as Entity Service does. The examples below use `BASE`, the Base URL from API's `config.yaml`, read in the API Component directory:

```sh
BASE=$(uv run python -c "import yaml; print(yaml.safe_load(open('config.yaml'))['url'])")
curl -s -X POST "$BASE/entity/currency/count" -H 'content-type: application/json' -d '{}'
# 8
```

## Endpoints

### Adapters

One Adapter for every Entity, beneath `$BASE/entity/<adapter>`, each holding the same twelve Endpoints for its own Entity:

| Entity | Adapter segment |
|---|---|
| User | `user` |
| Instance | `instance` |
| Currency | `currency` |
| Broker | `broker` |
| Asset | `asset` |
| Account Group | `account_group` |
| Account | `account` |

```sh
for adapter in user instance currency broker asset account_group account; do
  curl -s -X POST "$BASE/entity/$adapter/count" -H 'content-type: application/json' -d '{}'; echo " $adapter"
done
# 1 user
# 1 instance
# 8 currency
# 1 broker
# 4 asset
# 1 account_group
# 1 account
```

### Endpoints of every Adapter

Each Endpoint keeps its Action's Parameters, with the same names, requirements, and defaults. `id` travels in the Path. For `GET` and `DELETE`, the other Parameters travel in the Query; for `POST`, `PUT`, and `PATCH`, they travel in a JSON Body, each under its own name. An Entity travels as a JSON object of its fields; a Filter as `{"field", "operator", "value"}` and an Order as `{"field", "direction"}`, where `field` is the Field's name; `combination` and `direction` as member names; `instance` as its member name, `SQLITE`. `list`, `count`, `sum`, `min`, and `max` read, but take Filters, which a Query cannot carry, so they use `POST`.

| Method | Path | Parameters | Result |
|---|---|---|---|
| `POST` | `/add` | Body: `entity`, `instance` | The stored Entity |
| `PUT` | `/update` | Body: `entity`, `instance` | The stored Entity, or `null` |
| `POST` | `/list` | Body: `filters`, `combination`, `orders`, `limit`, `instance` | The matching Entities |
| `GET` | `/get_by_id/{id}` | Path: `id`; Query: `instance` | The Entity, or `null` |
| `DELETE` | `/delete/{id}` | Path: `id`; Query: `instance` | The deleted Entity, or `null` |
| `PATCH` | `/enable/{id}` | Path: `id`; Body: `instance` | The Entity, or `null` |
| `PATCH` | `/disable/{id}` | Path: `id`; Body: `instance` | The Entity, or `null` |
| `POST` | `/count` | Body: `filters`, `combination`, `instance` | The number of matching records |
| `POST` | `/sum` | Body: `field`, `filters`, `combination`, `instance` | The total, or zero |
| `POST` | `/min` | Body: `field`, `filters`, `combination`, `instance` | The smallest value, or `null` |
| `POST` | `/max` | Body: `field`, `filters`, `combination`, `instance` | The largest value, or `null` |
| `DELETE` | `/truncate` | Query: `instance` | The number of records removed |

Every Parameter except `entity`, `id`, and `field` is optional. One example for each, in order, on a freshly prepared database:

```sh
curl -s -X POST "$BASE/entity/broker/add" -H 'content-type: application/json' \
  -d '{"entity": {"name": "Example Broker", "user_id": 1}}'
# {"id": 2, "name": "Example Broker", "user_id": 1, "is_active": true, "description": null}
curl -s -X PUT "$BASE/entity/broker/update" -H 'content-type: application/json' \
  -d '{"entity": {"id": 2, "name": "Example Broker", "user_id": 1, "is_active": true, "description": "Updated"}}'
# {"id": 2, "name": "Example Broker", "user_id": 1, "is_active": true, "description": "Updated"}
curl -s -X POST "$BASE/entity/broker/list" -H 'content-type: application/json' \
  -d '{"filters": [{"field": "name", "operator": "STARTS_WITH", "value": "Example"}], "orders": [{"field": "id", "direction": "DESCENDING"}], "limit": 1}'
# [{"id": 2, "name": "Example Broker", "user_id": 1, "is_active": true, "description": "Updated"}]
curl -s "$BASE/entity/broker/get_by_id/2?instance=SQLITE"
# {"id": 2, "name": "Example Broker", "user_id": 1, "is_active": true, "description": "Updated"}
curl -s -X PATCH "$BASE/entity/broker/disable/2"
# {"id": 2, "name": "Example Broker", "user_id": 1, "is_active": false, "description": "Updated"}
curl -s -X PATCH "$BASE/entity/broker/enable/2" -H 'content-type: application/json' -d '{"instance": "SQLITE"}'
# {"id": 2, "name": "Example Broker", "user_id": 1, "is_active": true, "description": "Updated"}
curl -s -X DELETE "$BASE/entity/broker/delete/2"
# {"id": 2, "name": "Example Broker", "user_id": 1, "is_active": true, "description": "Updated"}
curl -s -X POST "$BASE/entity/currency/count" -H 'content-type: application/json' \
  -d '{"filters": [{"field": "decimal_digits", "operator": "EQUALS", "value": 0}, {"field": "code", "operator": "EQUALS", "value": "CHF"}], "combination": "OR"}'
# 2
curl -s -X POST "$BASE/entity/asset/sum" -H 'content-type: application/json' -d '{"field": "digits"}'
# 15
curl -s -X POST "$BASE/entity/asset/min" -H 'content-type: application/json' -d '{"field": "point_size"}'
# 0.0001
curl -s -X POST "$BASE/entity/asset/max" -H 'content-type: application/json' \
  -d '{"field": "digits", "filters": [{"field": "category", "operator": "EQUALS", "value": "Commodity"}]}'
# 3
```

`truncate` removes every record of its Entity. Here the Assets are removed and then put back by Database's `insert_initial_data` entry point, run in `../database`; they return with new ids:

```sh
curl -s -X DELETE "$BASE/entity/asset/truncate?instance=SQLITE"
# 4
(cd ../database && uv run python scripts/insert_initial_data.py > /dev/null)
curl -s -X POST "$BASE/entity/asset/count" -H 'content-type: application/json' -d '{}'
# 4
```

## Use

Send each request to `$BASE/entity/<adapter><path>` with the Method the table gives. Send a JSON Body with `content-type: application/json`, every Parameter under its own name; an omitted optional Parameter takes its Action's default. Results come back as JSON exactly as the Action returns them; an Entity in its own JSON form, with decimals as text.

Every error comes back as Problem Details (`application/problem+json`) whose `type` is the error's class name, with status 422 for invalid input, 503 for an inactive Instance or a connection failure, and 500 otherwise:

```sh
curl -s -X POST "$BASE/entity/asset/sum" -H 'content-type: application/json' -d '{"field": "symbol"}'
# {"type":"InvalidInputError","title":"InvalidInputError","status":422,"detail":"sum cannot use Asset.symbol of Type string"}
```

## Verify

With API running, check in the API Component directory that every Entity and every Action has exactly one Endpoint, and nothing else is served:

```python
import inspect
import json
import re
import urllib.request

import yaml
from logic.interface import Entity

base = yaml.safe_load(open("config.yaml"))["url"]
paths = json.load(urllib.request.urlopen(f"{base}/openapi.json"))["paths"]
served = {"/".join(path.split("/entity/", 1)[1].split("/")[:2]) for path in paths}
expected = set()
for name in [n for n in vars(Entity.Service) if not n.startswith("_")]:
    adapter = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    child = getattr(Entity.Service, name)
    for action in dir(child):
        if not action.startswith("_") and inspect.isfunction(getattr(child, action)):
            expected.add(f"{adapter}/{action}")
assert served == expected, served ^ expected
assert sum(len(operations) for operations in paths.values()) == len(expected)
print("verified")
```
