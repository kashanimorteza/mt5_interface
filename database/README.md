# Database

The project's storage library. It stores every Entity the Entity library publishes on a selected Instance, prepares that storage with the configured Initial Data, and offers all of it through one Interface.

## Overview

Database creates its Tables from the Entities themselves, keeps its storage inside this Component, and never exposes connection values. A consumer imports the Interface, creates `database_interface` once, and calls its Operations with imported Entities, Field references, and enumeration members, never strings:

```python
from database.interface import database_interface
from entity.interface import Broker

db = database_interface()
added = db.add(Broker(name="Example Broker", user_id=1))
print([broker.name for broker in db.list(Broker)])  # ['FxPro', 'Example Broker']
db.delete(Broker, added.id)  # leave the store as it was
```

## Interface

`database.interface` is the only module that publishes. It publishes exactly six groups, under Interface contract version `3.0`, and nothing else; every member is reached through its group:

```python
from database.interface import (
    database_error,
    database_instance,
    database_interface,
    database_result,
    database_setup,
    database_value,
)
```

### database_interface

Create it once with no argument; it holds every Entity Operation and the Command Operation. Every parameter after `entity`, `id`, `field`, and `command` is optional, and `instance` is always last: omit it to use the default Instance, or pass a `database_instance` member. An Entity is always the class or instance imported from `entity.interface`, and a Field is that class's attribute, such as `Broker.name`.

| Operation | Parameters | Effect and result |
|---|---|---|
| `add` | `entity`, `instance` | Stores one complete new Entity (its `id` still `None`) and returns it as stored, with its generated `id`. |
| `update` | `entity`, `instance` | Uses the Entity's `id` only to locate the record, replaces every mutable Field, and returns the stored Entity, or `None` when no record exists. `id` and immutable Fields never change. |
| `list` | `entity`, `filters`, `combination`, `orders`, `limit`, `instance` | Returns a list of the matching Entities. Omitted `filters` match everything, an omitted `combination` is `AND`, omitted `orders` sort by `id` ascending, and an omitted, zero, or negative `limit` means no limit. Supplied Orders replace the default and apply in their given sequence. |
| `get_by_id` | `entity`, `id`, `instance` | Returns the Entity with this `id`, or `None`. |
| `delete` | `entity`, `id`, `instance` | Deletes the record and returns the Entity as it was, or `None`. |
| `enable` | `entity`, `id`, `instance` | Sets only `is_active` to `True` and returns the final Entity, even when it was already enabled, or `None`. |
| `disable` | `entity`, `id`, `instance` | Sets only `is_active` to `False` and returns the final Entity, even when it was already disabled, or `None`. |
| `count` | `entity`, `filters`, `combination`, `instance` | Returns the number of matching records. |
| `sum` | `entity`, `field`, `filters`, `combination`, `instance` | Returns the total of one integer, float, or decimal Field over the matching records, ignoring nulls; zero (`0`, `0.0`, or `Decimal(0)`) when nothing matches. A decimal total is exact. |
| `min` | `entity`, `field`, `filters`, `combination`, `instance` | Returns the smallest value of one integer, float, decimal, string, datetime, date, or time Field, ignoring nulls; `None` when nothing matches. Decimals compare by value. |
| `max` | `entity`, `field`, `filters`, `combination`, `instance` | Returns the largest value, as `min` does. |
| `truncate` | `entity`, `instance` | Removes every record of the Entity, keeps its Table, and returns the deleted count. |
| `execute_command` | `command`, `parameters`, `instance` | Runs one native SQLite command with bound parameters (a mapping for `:name` placeholders or a sequence for `?`) and returns a `CommandResult`. It may also change the schema; `create_tables` remains the standard way to prepare it. |

Every change, and every native command, completes in one transaction or leaves no change at all.

`add`, `update`, `get_by_id`, `enable`, `disable`, and `delete`:

```python
from database.interface import database_interface
from entity.interface import Broker

db = database_interface()
broker = db.add(Broker(name="Example Broker", user_id=1, description="Added"))
broker.description = "Updated"
print(db.update(broker).description)  # Updated
print(db.disable(Broker, broker.id).is_active)  # False
print(db.enable(Broker, broker.id).is_active)  # True
print(db.get_by_id(Broker, broker.id).name)  # Example Broker
print(db.delete(Broker, broker.id).name)  # Example Broker
print(db.get_by_id(Broker, broker.id))  # None
```

`list` with every parameter:

```python
from database.interface import database_instance, database_interface, database_value
from entity.interface import Currency

db = database_interface()
currencies = db.list(
    Currency,
    filters=[
        database_value.Filter(
            Currency.decimal_digits, database_value.FilterOperator.EQUALS, 2
        ),
        database_value.Filter(
            Currency.code, database_value.FilterOperator.STARTS_WITH, "C"
        ),
    ],
    combination=database_value.FilterCombination.AND,
    orders=[
        database_value.Order(Currency.code, database_value.OrderDirection.DESCENDING)
    ],
    limit=1,
    instance=database_instance.SQLITE,
)
print([currency.code for currency in currencies])  # ['CHF']
```

`count`, `sum`, `min`, and `max`:

```python
from database.interface import database_interface, database_value
from entity.interface import Account, Asset

db = database_interface()
commodity = database_value.Filter(
    Asset.category, database_value.FilterOperator.EQUALS, "Commodity"
)
print(db.count(Asset, filters=[commodity]))  # 2
print(db.sum(Asset, Asset.digits))  # 15
print(db.min(Asset, Asset.point_size), db.max(Asset, Asset.point_size))  # 0.0001 0.01
print(db.sum(Account, Account.balance))  # 0
```

`truncate` removes every record of an Entity; here the Initial Data puts the Assets back afterwards:

```python
from database.interface import database_interface, database_setup
from entity.interface import Asset

db = database_interface()
print(db.truncate(Asset))  # 4
print(db.count(Asset))  # 0
database_setup().insert_initial_data()
print(db.count(Asset))  # 4
```

`execute_command`:

```python
from database.interface import database_interface

db = database_interface()
result = db.execute_command(
    "SELECT code, symbol FROM currency WHERE decimal_digits = :digits ORDER BY code",
    {"digits": 0},
)
print(result.rows, result.columns, result.success)
# ({'code': 'JPY', 'symbol': '¥'},) ('code', 'symbol') True
```

### database_setup

Create it with no argument; it holds the Setup Operations, each taking only an optional `instance` and returning a `SetupResult`. They are described in [Setup Operations](#setup-operations).

```python
from database.interface import database_setup

print(database_setup().create_tables().affected)  # 7
```

### database_value

What a consumer passes to an Operation. Each enumeration member's value equals its name.

- **`Filter(field, operator, value=None)`**: an immutable condition on one Field reference of the given Entity. `value` is omitted for `IS_NULL` and `IS_NOT_NULL`, is a list, tuple, or set for `IN`, and otherwise has the Field's own value category; an `int` is also accepted for a float or decimal Field.
- **`FilterOperator`**: `EQUALS`, `NOT_EQUALS`, `GREATER_THAN`, `GREATER_OR_EQUAL`, `LESS_THAN`, `LESS_OR_EQUAL` (integer, float, decimal, string, datetime, date, and time Fields), `IN`, `CONTAINS`, `STARTS_WITH`, `ENDS_WITH` (string Fields; case-sensitive and literal, so `%` and `_` match themselves), `IS_NULL`, `IS_NOT_NULL`.
- **`FilterCombination`**: `AND` (the default) or `OR`, joining all Filters of one call.
- **`Order(field, direction=OrderDirection.ASCENDING)`**: an immutable ordering by one Field reference.
- **`OrderDirection`**: `ASCENDING` (the default) or `DESCENDING`.

```python
from database.interface import database_interface, database_value
from entity.interface import Asset, Broker

db = database_interface()
value = database_value
print(
    [
        asset.symbol
        for asset in db.list(
            Asset,
            filters=[
                value.Filter(
                    Asset.symbol, value.FilterOperator.IN, ["EUR/USD", "USOil"]
                )
            ],
        )
    ]
)
# ['EUR/USD', 'USOil']
print(
    [
        asset.symbol
        for asset in db.list(
            Asset,
            filters=[value.Filter(Asset.symbol, value.FilterOperator.CONTAINS, "/")],
            orders=[value.Order(Asset.symbol)],
        )
    ]
)
# ['EUR/GBP', 'EUR/USD', 'XAU/USD']
print(
    db.count(
        Broker, filters=[value.Filter(Broker.description, value.FilterOperator.IS_NULL)]
    )
)  # 1
either = [
    value.Filter(Asset.digits, value.FilterOperator.GREATER_THAN, 4),
    value.Filter(Asset.point_size, value.FilterOperator.LESS_OR_EQUAL, 0.01),
]
print(db.count(Asset, filters=either, combination=value.FilterCombination.OR))  # 4
```

### database_instance

The active configured Instances, as an enumeration; it is itself the `DatabaseInstance` group. Today it has one member, `database_instance.SQLITE`. See [Instances](#instances).

```python
from database.interface import database_instance, database_interface
from entity.interface import User

print(list(database_instance))  # [<database_instance.SQLITE: 'sqlite'>]
print(database_interface().count(User, instance=database_instance.SQLITE))  # 1
```

### database_result

What a consumer reads back. Both are immutable.

- **`CommandResult`**: `rows` (a tuple of row mappings, or `None`), `affected` (the affected row count, or `None`), `columns` (the ordered column names, or `None`), `success`, `message`, and `instance` (the `database_instance` member used).
- **`SetupResult`**: `command` (the Setup Operation name), `instance`, `success`, `affected` (Tables for `create_tables`, Initial Data records for `insert_initial_data`, `None` for `prepare`), and `message`.

A result that is returned always has `success` `True`; a failure is raised as an error instead.

```python
from database.interface import database_interface, database_result

result = database_interface().execute_command(
    "UPDATE broker SET description = NULL WHERE id = ?", [1]
)
print(isinstance(result, database_result.CommandResult), result.affected)  # True 1
```

### database_error

Every error derives from `database_error.DatabaseError`. No error carries a connection value, a credential, or a stored value.

| Error | Raised when |
|---|---|
| `ConfigurationError` | The Database Configuration is missing or invalid, a configured record breaks its Entity contract, or `instance` is not a `database_instance` member. |
| `InactiveInstanceError` | The selected Instance is configured inactive. |
| `InvalidInputError` | An Entity, Field reference, Filter, Order, combination, limit, id, command, or parameters argument is invalid; raised before any storage is touched. |
| `DeclarationMismatchError` | An existing Table differs from its Entity, or a stored record does not satisfy its Entity contract. |
| `ConnectionFailureError` | The Instance's storage cannot be reached. |
| `ExecutionError` | A statement or native command fails, for example on a uniqueness or foreign-key constraint, or configured Initial Data conflicts with a stored record. |
| `SetupError` | `prepare` created the Tables but could not insert the Initial Data. |

```python
from database.interface import database_error, database_interface
from entity.interface import Broker

db = database_interface()
try:
    db.list("Broker")
except database_error.InvalidInputError as error:
    print(error)  # Expected an Entity class of the Entity Collection
try:
    db.add(Broker(name="FxPro", user_id=1))
except database_error.DatabaseError as error:
    print(type(error).__name__)  # ExecutionError
```

## Instances

`database_instance` has one member for every active Instance in `config.yaml` and none for an inactive one. Today `SQLITE` is active and is the default Instance (`settings.default_instance`); the configured PostgreSQL Instance is inactive, so it has no member. A call without `instance` runs on the default Instance; passing a member selects that Instance. Activating another Instance takes effect through `config.yaml` and the next generation of Database, which adds its member and, if its Engine is new, its Engine unit.

Connection values stay inside Database: a member carries only its Instance key, and no Result or error shows a host, password, or path. A file-backed Instance keeps its database file beneath the Database-owned `db/` directory of this Component, named by the Instance's database value; the default Instance's file is `db/application.db`. That location never depends on the working directory or the consumer.

## Setup

The library uses Python 3.14 or newer and `uv`. From this directory:

```sh
uv sync
```

This creates `.venv` and installs the library with its locked dependencies from `uv.lock`, including the Entity library from `../entity`.

Database reads its `config.yaml` and keeps its storage in this directory, so another Component of the repository depends on it through an editable local path dependency in its own `pyproject.toml`:

```toml
[project]
dependencies = ["database"]

[tool.uv.sources]
database = { path = "../database", editable = true }
```

Then prepare the default Instance once, as generation already does:

```sh
uv run python scripts/prepare.py
```

## Use

Every capability is used through the Interface groups, with Field references and enumeration members:

```python
from decimal import Decimal

from database.interface import database_interface, database_value
from entity.interface import Account, Currency

db = database_interface()

# Entity Operations
usd = db.list(
    Currency,
    filters=[
        database_value.Filter(
            Currency.code, database_value.FilterOperator.EQUALS, "USD"
        )
    ],
)[0]
print(usd.symbol)  # $

account = db.get_by_id(Account, 1)
account.balance = Decimal("1050.25")
print(db.update(account).balance)  # 1050.25
account.balance = Decimal("0")
db.update(account)

# Aggregates
print(
    db.count(
        Currency,
        filters=[
            database_value.Filter(
                Currency.decimal_digits, database_value.FilterOperator.LESS_THAN, 2
            )
        ],
    )
)  # 1

# Native command
print(db.execute_command("SELECT count(*) AS n FROM account").rows)  # ({'n': 1},)
```

## Setup Operations

Each Setup Operation runs on the selected Instance (the default when omitted), returns a `SetupResult`, and is also a script in `scripts/`, run by hand from this directory:

- **`create_tables`** (`uv run python scripts/create_tables.py`): creates every Table of the Entity Collection, with its columns, Primary Key, foreign keys, uniqueness constraints, and indexes, only from the Entities and their Declarations. Matching Tables are left unchanged, so it can run again. If an existing Table differs from its Entity, it stops with `DeclarationMismatchError`, names each difference, and changes nothing.
- **`insert_initial_data`** (`uv run python scripts/insert_initial_data.py`): checks every configured Initial Data record through its Entity first, then inserts the missing ones in one transaction and skips records already present. It never updates, deletes, or duplicates a record; a configured record that conflicts with a stored one on a uniqueness constraint fails with `ExecutionError` and nothing is inserted.
- **`prepare`** (`uv run python scripts/prepare.py`): runs `create_tables` and then `insert_initial_data`. When `create_tables` fails it stops before inserting anything; when the Initial Data fails after the Tables were created it raises `SetupError`.

Generation runs `prepare` on the default Instance automatically after it generates Database. Each script prints its `SetupResult` and exits with status 0, or prints the error and exits with status 1. Other Instances are prepared only when selected explicitly:

```python
from database.interface import database_instance, database_setup

result = database_setup().prepare(instance=database_instance.SQLITE)
print(result.command, result.success)  # prepare True
print(result.message)
# All 7 Entity Tables are present and match their Entities. 0 Initial Data records inserted, 17 already present.
```

## Initial Data

The Initial Data is the `initial_data` collection of `config.yaml`, copied from the Target. Database inserts every value unchanged, without hashing, encryption, masking, or omission because a Field is a credential. A value the Target leaves to be generated securely is copied as an empty string; Database never generates it, and you fill it in yourself.

| Entity | Records |
|---|---|
| User | `name` Admin, `username` admin, `password` and `api_key` empty |
| Instance | `name` MetaTrader, `user_id` 1, `ip` 127.0.0.1, `path` C:\Program Files\FxPro Markets MT5\terminal64.exe, `username` test, `password` and `api_key` empty |
| Currency | `user_id` 1 for each: USD `$` United States 2; EUR `€` Eurozone 2; GBP `£` United Kingdom 2; JPY `¥` Japan 0; CHF `CHF` Switzerland 2; CAD `C$` Canada 2; AUD `A$` Australia 2; NZD `NZ$` New Zealand 2 (`code`, `symbol`, `country`, `decimal_digits`) |
| Broker | `name` FxPro, `user_id` 1 |
| Asset | `broker_id` 1 for each: EUR/USD Currency 0.0001 5; EUR/GBP Currency 0.001 5; XAU/USD Commodity 0.01 2; USOil Commodity 0.01 3 (`symbol`, `category`, `point_size`, `digits`) |
| Account Group | `user_id` 1, `name` Default |
| Account | `name` Acc-1, `group_id` 1, `broker_id` 1, `instance_id` 1, `base_currency_id` 1, `username` test, `password` empty, `leverage` 100, `account_type` CFD |

## Verify

From this directory:

```sh
uv sync --locked
uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run python scripts/prepare.py
ls db/application.db
```

Running `prepare` again succeeds and reports every Initial Data record as already present. Then, in a fresh interpreter, check the published shape and each capability group:

```python
import gc
import os

before = sorted(os.listdir("db"))

import sqlalchemy  # noqa: E402

import database.interface as interface  # noqa: E402
from database.interface import (  # noqa: E402
    database_error,
    database_instance,
    database_interface,
    database_result,
    database_setup,
    database_value,
)
from entity.interface import Asset, Broker, entities  # noqa: E402

# Loading the Interface opens no connection and creates no file.
assert sorted(os.listdir("db")) == before
assert not [item for item in gc.get_objects() if isinstance(item, sqlalchemy.Engine)]

# It publishes exactly the six groups.
assert sorted(interface.__all__) == sorted(
    [
        "database_error",
        "database_instance",
        "database_interface",
        "database_result",
        "database_setup",
        "database_value",
    ]
)
assert [member.name for member in database_instance] == ["SQLITE"]
assert [member.name for member in database_value.FilterOperator] == [
    "EQUALS",
    "NOT_EQUALS",
    "GREATER_THAN",
    "GREATER_OR_EQUAL",
    "LESS_THAN",
    "LESS_OR_EQUAL",
    "IN",
    "CONTAINS",
    "STARTS_WITH",
    "ENDS_WITH",
    "IS_NULL",
    "IS_NOT_NULL",
]
assert [member.name for member in database_value.FilterCombination] == ["AND", "OR"]
assert [member.name for member in database_value.OrderDirection] == [
    "ASCENDING",
    "DESCENDING",
]

db = database_interface()
assert db.count(Asset) == db.count(Asset, instance=database_instance.SQLITE) == 4
broker = db.add(Broker(name="Verify Broker", user_id=1))
assert db.disable(Broker, broker.id).is_active is False
assert db.delete(Broker, broker.id).name == "Verify Broker"
assert db.get_by_id(Broker, broker.id) is None
assert db.sum(Asset, Asset.digits) == 15
assert isinstance(db.execute_command("SELECT 1 AS one"), database_result.CommandResult)
for wrong in (
    lambda: db.list("Asset"),
    lambda: db.count(
        Asset,
        filters=[
            database_value.Filter("symbol", database_value.FilterOperator.EQUALS, "x")
        ],
    ),
):
    try:
        wrong()
        raise AssertionError("a string was accepted")
    except database_error.InvalidInputError:
        pass

again = database_setup().prepare()
assert again.success and "17 already present" in again.message
assert os.path.isfile("db/application.db")
assert [entity.declaration.name for entity in entities][-1] == "Account"
print("verified")
```

## Troubleshooting

- **`InactiveInstanceError`**: the selected Instance is set `active: false` in `config.yaml`. Activate it there and regenerate Database, or select an active member.
- **`ConfigurationError` naming `settings.default_instance`**: the default Instance must be active and configured. **`ConfigurationError` saying `config.yaml` is missing**: Database was installed as a copy rather than used from this directory; depend on it with `editable = true` as shown in [Setup](#setup).
- **`ConfigurationError` saying an active Instance has no DatabaseInstance member**: `config.yaml` activates an Instance that this generation of Database does not know; regenerate Database.
- **`DeclarationMismatchError` from `create_tables` or `prepare`**: an existing Table differs from its Entity, for example after an Entity changed. Database never alters an existing Table; bring the stored Table in line with the Entity, or start from an empty database file, then run `prepare` again.
- **`ExecutionError` from `insert_initial_data` naming a conflict**: a stored record shares a uniqueness constraint with a configured Initial Data record but differs from it, for example after an Initial Data value was edited in storage. Make the stored record and `config.yaml` agree, then run it again.
- **Empty Initial Data values**: User, Instance, and Account credentials are stored as empty strings because the Target asks for securely generated values, which Database never produces. Fill them in `config.yaml` before the first `prepare`, or later through your own code; once stored, a changed value in `config.yaml` conflicts with the stored record.
- **`ConnectionFailureError`**: the storage directory or database file cannot be created or opened; check the permissions of `db/`.
