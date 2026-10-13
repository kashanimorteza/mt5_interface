# Entity Service

## Overview

Entity Service gives every Entity one Child Service. A caller selects an Entity once by choosing its Child Service, then calls its Actions without passing the Entity again; every Action is one of Database's Entity Operations, forwarded through Database Interface and answered exactly as Database answers. Everything a caller needs comes from this Service's Interface, so it never imports Entity or Database itself:

```python
from logic.services.entity.interface import Service

print([currency.code for currency in Service.Currency().list(limit=3)])
# ['USD', 'EUR', 'GBP']
```

Inside Logic, reach it as `Entity` through Logic Interface: `from logic.interface import Entity`, then `Entity.Service.Currency()`.

## Interface

`logic.services.entity.interface` publishes exactly five names, under Interface contract version `3.0`, and nothing else: `Service`, `Entity`, `database_value`, `database_instance`, and `database_error`. Loading it opens no connection and creates no data or file.

### Service

One Child Service for every Entity of the Entity Collection, in its order: `User`, `Instance`, `Currency`, `Broker`, `Asset`, `AccountGroup`, and `Account`. Create a Child Service with no argument; it holds one Database object that all its Actions use.

```python
from logic.services.entity.interface import Service

print(Service.User().count())  # 1
print(Service.Instance().count())  # 1
print(Service.Currency().count())  # 8
print(Service.Broker().count())  # 1
print(Service.Asset().count())  # 4
print(Service.AccountGroup().count())  # 1
print(Service.Account().count())  # 1
```

Every Child Service has the same twelve Actions, in Database's order. Each has its Database Entity Operation's name, parameters, defaults, result, and errors, without the Entity class, which the Child Service supplies; `add` and `update` keep their Entity instance and refuse an instance of another Entity with `database_error.InvalidInputError` before Database is called.

| Action | Parameters | Result |
|---|---|---|
| `add` | `entity`, `instance` | The stored Entity, with its generated `id`. |
| `update` | `entity`, `instance` | The stored Entity after every mutable Field is replaced, or `None` when no record has its `id`. |
| `list` | `filters`, `combination`, `orders`, `limit`, `instance` | The matching Entities; by default all of them, ordered by `id`. |
| `get_by_id` | `id`, `instance` | The Entity, or `None`. |
| `delete` | `id`, `instance` | The deleted Entity as it was, or `None`. |
| `enable` | `id`, `instance` | The Entity with `is_active` set to `True`, or `None`. |
| `disable` | `id`, `instance` | The Entity with `is_active` set to `False`, or `None`. |
| `count` | `filters`, `combination`, `instance` | The number of matching records. |
| `sum` | `field`, `filters`, `combination`, `instance` | The total of one numeric Field, or zero. |
| `min` | `field`, `filters`, `combination`, `instance` | The smallest value of one Field, or `None`. |
| `max` | `field`, `filters`, `combination`, `instance` | The largest value of one Field, or `None`. |
| `truncate` | `instance` | The number of records removed; the Table stays. |

```python
from logic.services.entity.interface import Entity, Service, database_value

brokers = Service.Broker()
added = brokers.add(Entity.Broker(name="Example Broker", user_id=1))
added.description = "Example"
print(brokers.update(added).description)  # Example
print([broker.name for broker in brokers.list()])  # ['FxPro', 'Example Broker']
print(brokers.get_by_id(added.id).name)  # Example Broker
print(brokers.disable(added.id).is_active)  # False
print(brokers.enable(added.id).is_active)  # True
print(brokers.delete(added.id).name)  # Example Broker

assets = Service.Asset()
currency = database_value.Filter(
    Entity.Asset.category, database_value.FilterOperator.EQUALS, "Currency"
)
print(assets.count(filters=[currency]))  # 2
print(assets.sum(Entity.Asset.digits))  # 15
print(assets.min(Entity.Asset.point_size), assets.max(Entity.Asset.point_size))
# 0.0001 0.01
```

`truncate` removes every record of its Entity. Here the removed Assets are added back afterwards, with new ids:

```python
from logic.services.entity.interface import Entity, Service

assets = Service.Asset()
saved = assets.list()
print(assets.truncate())  # 4
for asset in saved:
    fields = Entity.Asset.declaration.fields
    assets.add(
        Entity.Asset(
            **{f.name: getattr(asset, f.name) for f in fields if f.name != "id"}
        )
    )
print(assets.count())  # 4
```

### Entity

The Entity each Child Service binds, under the Child Service's name: `Entity.User`, `Entity.Instance`, `Entity.Currency`, `Entity.Broker`, `Entity.Asset`, `Entity.AccountGroup`, and `Entity.Account`. Each is the Entity Component's own object, so a caller builds new records with it and uses its class attributes as Field references.

```python
from logic.services.entity.interface import Entity

print(
    [
        item.declaration.name
        for item in (
            Entity.User,
            Entity.Instance,
            Entity.Currency,
            Entity.Broker,
            Entity.Asset,
            Entity.AccountGroup,
            Entity.Account,
        )
    ]
)
# ['User', 'Instance', 'Currency', 'Broker', 'Asset', 'Account Group', 'Account']
```

### database_value

Database's Value group, unchanged: `Filter`, `FilterOperator`, `FilterCombination`, `Order`, and `OrderDirection`, used exactly as Database documents them.

```python
from logic.services.entity.interface import Entity, Service, database_value

value = database_value
currencies = Service.Currency().list(
    filters=[
        value.Filter(Entity.Currency.decimal_digits, value.FilterOperator.EQUALS, 0),
        value.Filter(Entity.Currency.code, value.FilterOperator.EQUALS, "CHF"),
    ],
    combination=value.FilterCombination.OR,
    orders=[value.Order(Entity.Currency.code, value.OrderDirection.DESCENDING)],
)
print([currency.code for currency in currencies])  # ['JPY', 'CHF']
```

### database_instance

Database's Instance group, unchanged; today its only member is `SQLITE`, Database's default Instance. Omit `instance` to use the default.

```python
from logic.services.entity.interface import Service, database_instance

print(Service.Broker().count(instance=database_instance.SQLITE))  # 1
```

### database_error

Database's Error group, unchanged: `DatabaseError` and its kinds `ConfigurationError`, `InactiveInstanceError`, `InvalidInputError`, `DeclarationMismatchError`, `ConnectionFailureError`, `ExecutionError`, and `SetupError`. Every Action raises them exactly as Database does.

```python
from logic.services.entity.interface import Entity, Service, database_error

try:
    Service.User().add(Entity.Broker(name="Wrong", user_id=1))
except database_error.InvalidInputError as error:
    print(error)  # Expected an instance of User
try:
    Service.Broker().add(Entity.Broker(name="FxPro", user_id=1))
except database_error.DatabaseError as error:
    print(type(error).__name__)  # ExecutionError
```

An `instance` that is not a `database_instance` member raises `ConfigurationError`. `InactiveInstanceError`, `DeclarationMismatchError`, and `ConnectionFailureError` come from Database's configuration, its stored data, or its storage, and `SetupError` only from Database's own Setup Operations, which Entity Service does not offer. Each kind is told apart by its class:

```python
from logic.services.entity.interface import Service, database_error


def explain(error: database_error.DatabaseError) -> str:
    match error:
        case database_error.ConfigurationError():
            return "check Database's config.yaml or the instance argument"
        case database_error.InactiveInstanceError():
            return "select an active Instance"
        case database_error.InvalidInputError():
            return "fix the call's arguments"
        case database_error.DeclarationMismatchError():
            return "a stored record or Table differs from its Entity"
        case database_error.ConnectionFailureError():
            return "Database's storage cannot be reached"
        case database_error.ExecutionError():
            return "the statement failed, for example on a uniqueness rule"
        case database_error.SetupError():
            return "Database's preparation is incomplete"
    return "another Database error"


try:
    Service.User().count(instance="sqlite")
except database_error.DatabaseError as error:
    print(type(error).__name__, "-", explain(error))
# ConfigurationError - check Database's config.yaml or the instance argument
```

## Use

Import the Child Service you need and its Entity from this Service's Interface, or through Logic Interface:

```python
from logic.interface import Entity

accounts = Entity.Service.Account()
print([account.name for account in accounts.list()])  # ['Acc-1']
```

Every Child Service lives in its own unit beside Base and inherits Base's Actions. Behavior that belongs to one Entity only is added in that Entity's Child Service, as a new Action or an override of a Base Action that applies to that Entity alone; anything shared belongs to Base, whose Actions follow Database's Interface group one to one.

## Verify

From the Logic Component directory, check in a fresh interpreter that Entity Service matches the Entity Collection and Database's Interface group:

```python
import inspect

from database import interface as database
from entity import interface as entity

from logic.services.entity import interface
from logic.services.entity.base import BaseEntity

names = [item.__name__ for item in entity.entities]
assert sorted(interface.__all__) == sorted(
    ["Entity", "Service", "database_error", "database_instance", "database_value"]
)
assert [n for n in vars(interface.Service) if not n.startswith("_")] == names
assert all(
    getattr(interface.Entity, n) is item for n, item in zip(names, entity.entities)
)
assert all(
    getattr(interface.Service, n)._entity is item
    for n, item in zip(names, entity.entities)
)
for group in ("database_value", "database_instance", "database_error"):
    assert getattr(interface, group) is getattr(database, group)

operations = [
    name
    for name, function in vars(database.database_interface).items()
    if not name.startswith("_")
    and list(inspect.signature(function).parameters)[1] == "entity"
]
actions = [name for name in vars(BaseEntity) if not name.startswith("_")]
assert actions == operations
assert "execute_command" not in actions
print("verified")
```
