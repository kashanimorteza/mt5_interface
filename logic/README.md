# Logic

## Overview

Logic is the project's reusable library of Behavior. Its work is divided into Services, each owning one responsibility, and Logic Interface publishes every Service's own Interface under the Service's name, so a consumer finds every Service in one place without knowing where it lives inside Logic. Logic starts no process and owns no transport; the API Component uses it as a library.

```python
from logic.interface import Entity

print(Entity.Service.User().count())  # 1
```

## Interface

`logic.interface` is the only module that publishes. Under Interface contract version `1.1` it publishes one name per Service and nothing else:

| Name | What it is |
|---|---|
| `Entity` | The Entity Service Interface itself: one Child Service per Entity, the Entities they bind, and Database's Value, Instance, and Error groups. |

## Services

- **Entity** (`Entity`): [README](logic/services/entity/README.md), [Definition](../.interface/implementation/development/logic/services/entity/entity.md), [Preferences](../.interface/implementation/development/logic/services/entity/entity.yaml).

The MT5 Service named by the Target is reserved and not yet defined, so Logic does not publish it yet.

## Setup

Logic uses Python 3.14 or newer and `uv`, and depends on the Entity and Database Components beside it in this repository. From this directory:

```sh
uv sync
```

This creates `.venv` with Logic, the Entity library from `../entity`, and the Database library from `../database` as an editable dependency, so that Database keeps using its own Configuration and storage. Prepare Database's default Instance once before use, from `../database`:

```sh
uv run python scripts/prepare.py
```

Another Component of this repository depends on Logic through a local path dependency in its own `pyproject.toml`:

```toml
[project]
dependencies = ["logic"]

[tool.uv.sources]
logic = { path = "../logic" }
database = { path = "../database", editable = true }
```

## Use

Import from Logic Interface only, and select a Service by its name:

```python
from logic.interface import Entity

currencies = Entity.Service.Currency()
usd = currencies.list(
    filters=[
        Entity.database_value.Filter(
            Entity.Entity.Currency.code,
            Entity.database_value.FilterOperator.EQUALS,
            "USD",
        )
    ]
)
print(usd[0].symbol)  # $
```

## Verify

From this directory:

```sh
uv sync --locked
uv run ruff format --check .
uv run ruff check .
uv run ty check
```

Then check in a fresh interpreter that Logic Interface publishes exactly every listed Service, each as its own Interface:

```python
import logic.interface as interface
from logic.services.entity import interface as entity_service

assert interface.__all__ == ["Entity"]
assert interface.Entity is entity_service
print("verified")
```

## Troubleshooting

- **`database_error.ConfigurationError` saying `config.yaml` is missing**: Database was installed as a copy instead of from `../database`. Keep `database = { path = "../database", editable = true }` in the consumer's `[tool.uv.sources]` and run `uv sync` again.
- **`database_error.ExecutionError` with `no such table`**: Database's default Instance has not been prepared. Run `uv run python scripts/prepare.py` in `../database`.
- **`database_error.InvalidInputError` saying `Expected an instance of ...`**: an Entity instance was given to another Entity's Child Service. Use the Child Service of the same name, such as `Entity.Service.Broker()` for `Entity.Entity.Broker`.
- **A change in Entity or Database does not show up**: the Entity library is installed as a copy; run `uv sync` again after it changes.
