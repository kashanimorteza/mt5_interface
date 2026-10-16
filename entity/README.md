# Entity

The project's reusable data-model library. It defines every Entity once, in a technology-independent Declaration, and publishes each Entity through one Interface.

## Overview

Every Entity is a flat, strictly validated model that carries its own public Declaration and converts losslessly to and from JSON text.

```python
from entity.interface import Currency

usd = Currency(user_id=1, code="USD", symbol="$", country="United States")
print(usd.code, usd.decimal_digits)  # USD 2
```

## Interface

`entity.interface` is the only module that publishes. It publishes two forms and nothing else, under Interface contract version `2.1`:

- **Entity Exports**: each Entity on its own, by its own name.
- **Entity Collection**: `entities`, an immutable tuple holding every Entity once, in Target order.

Import one Entity directly:

```python
from entity.interface import Account
```

Or work with all of them through the Entity Collection:

```python
from entity.interface import entities

for item in entities:
    print(item.declaration.name, len(item.declaration.fields))
```

Each Entity is listed below in Target order.

### User

Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.

| Field | Type | Nullable | Default | Value Generation | Sensitivity | Immutable | Constraints | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | auto_increment | — | yes | — | — |
| `name` | string | no | — | — | — | no | — | The user's display name. |
| `username` | string | no | — | — | — | no | — | The username used to identify the user. |
| `password` | string | no | — | — | password | no | — | The password credential used by the user. |
| `api_key` | string | no | — | — | sensitive | no | — | The API key assigned to the user. |
| `is_active` | boolean | no | `true` | — | — | no | — | Indicates whether the user is active. |
| `description` | string | yes | — | — | — | no | — | Describes the user. |

- **Primary Key:** `id`
- **Relations:** none
- **Uniqueness Constraints:** (`name`), (`username`)
- **Indexes:** none

### Instance

Defines a user-owned connection instance through which the system accesses MetaTrader 5.

| Field | Type | Nullable | Default | Value Generation | Sensitivity | Immutable | Constraints | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | auto_increment | — | yes | — | — |
| `user_id` | integer | no | — | — | — | no | — | Identifies the user who owns this instance. |
| `name` | string | no | — | — | — | no | — | The instance's display name. |
| `ip` | string | yes | — | — | — | no | — | Identifies the technical network address used to reach MetaTrader 5 when required. |
| `path` | string | yes | — | — | — | no | — | The local filesystem path of the MetaTrader 5 terminal executable used by this Instance when required. |
| `username` | string | yes | — | — | — | no | — | Defines the technical username used to establish the Instance connection when required. |
| `password` | string | yes | — | — | password | no | — | Defines the technical password used to establish the Instance connection when required. |
| `api_key` | string | yes | — | — | sensitive | no | — | Defines the technical API credential used to establish the Instance connection when required. |
| `is_active` | boolean | no | `true` | — | — | no | — | Indicates whether the instance is active. |
| `description` | string | yes | — | — | — | no | — | Describes the instance. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Currency

Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.

| Field | Type | Nullable | Default | Value Generation | Sensitivity | Immutable | Constraints | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | auto_increment | — | yes | — | — |
| `user_id` | integer | no | — | — | — | no | — | Identifies the user who owns this currency. |
| `code` | string | no | — | — | — | no | size 3 | The currency's standard three-letter code, such as `USD` or `EUR`. |
| `symbol` | string | yes | — | — | — | no | — | The currency's display symbol, such as `$`, `€`, or `£`. |
| `country` | string | yes | — | — | — | no | — | Identifies the country or region associated with the currency. |
| `decimal_digits` | integer | no | `2` | — | — | no | — | Defines the number of decimal digits normally used for monetary values in the currency. |
| `is_active` | boolean | no | `true` | — | — | no | — | Indicates whether the currency is active. |
| `description` | string | yes | — | — | — | no | — | Describes the currency. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `code`)
- **Indexes:** none

### Broker

Defines a broker supported by the system and identifies the user who owns its configuration.

| Field | Type | Nullable | Default | Value Generation | Sensitivity | Immutable | Constraints | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | auto_increment | — | yes | — | — |
| `name` | string | no | — | — | — | no | — | The broker's display name. |
| `user_id` | integer | no | — | — | — | no | — | Identifies the user who owns the broker configuration. |
| `is_active` | boolean | no | `true` | — | — | no | — | Indicates whether the broker is active. |
| `description` | string | yes | — | — | — | no | — | Describes the broker. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Asset

Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.

| Field | Type | Nullable | Default | Value Generation | Sensitivity | Immutable | Constraints | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | auto_increment | — | yes | — | — |
| `broker_id` | integer | no | — | — | — | no | — | Identifies the broker that provides this asset. |
| `symbol` | string | no | — | — | — | no | — | Identifies the tradable asset, such as `EUR/USD`, `XAU/USD`, or `USOil`. |
| `category` | string | no | — | — | — | no | — | Identifies the asset category, such as `Currency`, `Commodity`, or `Cryptocurrency`. |
| `point_size` | float | no | `0.0` | — | — | no | — | Stores the size of one point for the asset. |
| `digits` | integer | no | `0` | — | — | no | — | Stores the number of decimal digits used for the asset's price. |
| `is_active` | boolean | no | `true` | — | — | no | — | Indicates whether the asset is active. |
| `description` | string | yes | — | — | — | no | — | Describes the asset. |

- **Primary Key:** `id`
- **Relations:** `broker_id` → Broker.`id`
- **Uniqueness Constraints:** (`broker_id`, `symbol`)
- **Indexes:** none

### Account Group

Defines an independent group for organizing trading accounts owned by one user.

| Field | Type | Nullable | Default | Value Generation | Sensitivity | Immutable | Constraints | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | auto_increment | — | yes | — | — |
| `user_id` | integer | no | — | — | — | no | — | Identifies the user who owns the account group. |
| `name` | string | no | — | — | — | no | — | The account group's display name. |
| `is_active` | boolean | no | `true` | — | — | no | — | Indicates whether the account group is active. |
| `description` | string | yes | — | — | — | no | — | Describes the account group. |

- **Primary Key:** `id`
- **Relations:** `user_id` → User.`id`
- **Uniqueness Constraints:** (`user_id`, `name`)
- **Indexes:** none

### Account

Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to MetaTrader 5.

| Field | Type | Nullable | Default | Value Generation | Sensitivity | Immutable | Constraints | Description |
|---|---|---|---|---|---|---|---|---|
| `id` | integer | no | — | auto_increment | — | yes | — | — |
| `name` | string | no | — | — | — | no | — | The account's display name. |
| `group_id` | integer | no | — | — | — | no | — | Identifies the account group that contains the account. |
| `broker_id` | integer | no | — | — | — | no | — | Identifies the broker that owns the account. |
| `instance_id` | integer | no | — | — | — | no | — | Identifies the trading-platform instance used to connect this account. |
| `base_currency_id` | integer | no | — | — | — | no | — | Identifies the base currency used by the account. |
| `username` | string | no | — | — | — | no | — | The username identifier used to access the trading account. |
| `password` | string | no | — | — | password | no | — | The credential used to access the trading account. |
| `leverage` | integer | no | — | — | — | no | — | Defines the account's leverage multiplier. |
| `balance` | decimal | no | `0` | — | — | no | — | Stores the account's current balance. |
| `account_type` | string | no | — | — | — | no | — | Identifies the account model, such as `cfd` or `spread_betting`. |
| `is_active` | boolean | no | `true` | — | — | no | — | Indicates whether the account is active. |
| `description` | string | yes | — | — | — | no | — | Describes the account. |

- **Primary Key:** `id`
- **Relations:** `group_id` → Account Group.`id`, `broker_id` → Broker.`id`, `instance_id` → Instance.`id`, `base_currency_id` → Currency.`id`
- **Uniqueness Constraints:** (`name`), (`group_id`, `broker_id`, `instance_id`)
- **Indexes:** none

A nullable Field with no Default Value may be omitted; it is then null. Every non-nullable Field with no Default Value and no Value Generation is required.

## Declaration

Every Entity exposes its public Declaration as the class attribute `declaration`, an immutable record of its name, description, ordered Fields, and Entity Metadata:

```python
from entity.interface import Account

declaration = Account.declaration
print(declaration.name)  # Account
print([field.name for field in declaration.fields][:3])  # ['id', 'name', 'group_id']
print(declaration.primary_key)  # id

for relation in declaration.relations:
    print(relation.local_field, "->", relation.target_entity, relation.target_field)

print([constraint.fields for constraint in declaration.unique_constraints])
print([index.fields for index in declaration.indexes])  # []

password = next(field for field in declaration.fields if field.name == "password")
print(password.type, password.nullable, password.sensitivity)  # string False password
```

A Field Declaration exposes `name`, `type`, `nullable`, `description`, `default`, `sensitivity`, `immutable`, `constraints`, and `value_generation`. An absent Default Value is `NO_DEFAULT`, which is distinct from an explicit `None` default:

```python
from entity.core.declaration import NO_DEFAULT
from entity.interface import User

name = next(field for field in User.declaration.fields if field.name == "name")
print(name.default is NO_DEFAULT)  # True
```

## Foundation

Every Entity extends `Foundation`, which provides two conversions.

`to_json` returns JSON text with one root object whose keys are exactly the Entity's Fields, in Declaration order:

```python
from entity.interface import Broker

broker = Broker(name="Example Broker", user_id=1)
print(broker.to_json())
# {"id": null, "name": "Example Broker", "user_id": 1, "is_active": true, "description": null}
```

`from_json` builds the Entity from JSON text with the same rules as direct construction. It also accepts an `id` that storage has already assigned:

```python
from entity.interface import Broker

stored = Broker.from_json(
    '{"id": 7, "name": "Example Broker", "user_id": 1, "is_active": true, "description": null}'
)
print(stored.id)  # 7
```

A complete round trip, keeping an exact decimal:

```python
from decimal import Decimal

from entity.interface import Account

account = Account(
    name="Example",
    group_id=1,
    broker_id=1,
    instance_id=1,
    base_currency_id=1,
    username="example-user",
    password="example-password",
    leverage=100,
    balance=Decimal("1050.25"),
    account_type="CFD",
)
restored = Account.from_json(account.to_json())
print(restored == account, restored.balance)  # True 1050.25
```

## Setup

The library uses Python 3.14 or newer and `uv`. From this directory:

```sh
uv sync
```

This creates `.venv` and installs the library together with its locked dependencies from `uv.lock`.

Another Component in this repository depends on it through a local path dependency in its own `pyproject.toml`:

```toml
[project]
dependencies = ["entity"]

[tool.uv.sources]
entity = { path = "../entity" }
```

## Use

Build an Entity by direct construction. Validation is strict: an undeclared Field, a value of the wrong Type, and a missing required Field are all refused, and no value is coerced:

```python
from pydantic import ValidationError

from entity.interface import Asset

asset = Asset(
    broker_id=1, symbol="EUR/USD", category="Currency", point_size=0.0001, digits=5
)
print(asset.id)  # None: storage assigns it

try:
    Asset(broker_id=1, symbol="EUR/USD", category="Currency", point_size=1)
except ValidationError as error:
    print(error.errors()[0]["type"])  # float_type
```

Assigning to a mutable Field validates the whole Entity first. A failed assignment keeps the prior value, and `id` can never be assigned:

```python
from pydantic import ValidationError

from entity.interface import AccountGroup

group = AccountGroup(user_id=1, name="Default")
group.is_active = False

try:
    group.name = None
except ValidationError:
    print(group.name)  # Default

try:
    group.id = 1
except ValidationError as error:
    print(error.errors()[0]["type"])  # frozen_field
```

In every validation message, a Field with a Sensitivity Marker has its input replaced:

```python
from pydantic import ValidationError

from entity.interface import User

try:
    User(name="Example", username="example", password=123, api_key="example-key")
except ValidationError as error:
    print(error.errors()[0]["input"])  # **********
```

Each Entity also carries its table-ready form. A storage consumer reaches the shared table metadata through any Entity, as `User.metadata`; it holds exactly the Entities' tables. Entity itself never runs storage.

## Verify

From this directory:

```sh
uv sync
uv run ruff format --check .
uv run ruff check .
uv run ty check
```

Then, in a fresh interpreter, check the published shape and behaviour:

```python
import dataclasses
import gc
import threading

from pydantic import ValidationError

threads = threading.active_count()

import entity.interface as interface  # noqa: E402
from entity.core.declaration import Declaration  # noqa: E402
from entity.core.foundation import Foundation  # noqa: E402
from entity.interface import User, entities  # noqa: E402

# Loading the Interface has no side effect.
assert not [item for item in gc.get_objects() if isinstance(item, Foundation)]
assert threading.active_count() == threads

names = ["User", "Instance", "Currency", "Broker", "Asset", "AccountGroup", "Account"]
assert [item.__name__ for item in entities] == names
assert isinstance(entities, tuple)
assert all(getattr(interface, name) is item for name, item in zip(names, entities))
assert sorted(interface.__all__) == sorted([*names, "entities"])
assert [item.declaration.name for item in entities][5] == "Account Group"

# Each Entity exposes its actual, immutable Declaration.
for name, item in zip(names, entities):
    assert type(item.declaration) is Declaration
    assert getattr(interface, name).declaration is item.declaration
    try:
        item.declaration.name = "changed"
        raise AssertionError("mutable Declaration")
    except dataclasses.FrozenInstanceError:
        pass

user = User(
    name="Example",
    username="example",
    password="example-password",
    api_key="example-key",
)
assert User.from_json(user.to_json()) == user
for bad in ({"unknown": 1}, {"name": 1}, {"id": 1}):
    try:
        User(
            **{
                "name": "Example",
                "username": "example",
                "password": "x",
                "api_key": "y",
                **bad,
            }
        )
        raise AssertionError(bad)
    except ValidationError:
        pass
try:
    user.id = 1
    raise AssertionError("id assigned")
except ValidationError:
    pass
try:
    hash(user)
    raise AssertionError("hashable")
except TypeError:
    pass
print("verified")
```

## Troubleshooting

- **`ValidationError` with `float_type` for an integer value**: a float Field accepts only a finite `float`. Pass `1.0`, not `1`.
- **`ValidationError` with `datetime` or `decimal` input**: datetimes must be timezone-aware, and decimals must be `decimal.Decimal`. In JSON text, both are strings.
- **`ValidationError` with `auto_increment` on `id`**: `id` is assigned by storage. Omit it when constructing an Entity directly; `from_json` accepts a stored value.
- **`ValidationError` with `frozen_field`**: `id` is immutable once set and cannot be assigned.
- **`TypeError: unhashable type`**: Entities are mutable and deliberately not hashable. Key collections by `id` instead.
- **`TypeError` while importing an Entity**: its type name, table name, or Fields no longer match its Declaration. Bring the Entity unit back in line with its Declaration.
