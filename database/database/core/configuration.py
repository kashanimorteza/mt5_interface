"""Loading and validating the Database Configuration, the sole runtime source of Instances."""

from collections.abc import Collection, Mapping
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

import yaml
from entity.interface import entities

from database.core.errors import ConfigurationError
from database.core.values import FilterCombination, OrderDirection, database_instance

COMPONENT_ROOT = Path(__file__).resolve().parents[2]
"""The Database Component directory that holds the Configuration and Storage."""

CONFIGURATION_FILE = "config.yaml"

_SECTIONS = ("engines", "instances", "settings", "initial_data")
_ENGINE_PARAMETERS = (
    "storage",
    "required_parameters",
    "foreign_keys",
    "connect_arguments",
    "default_port",
)
_INSTANCE_FIELDS = (
    "name",
    "active",
    "engine",
    "host",
    "port",
    "database",
    "username",
    "password",
    "options",
)


@dataclass(frozen=True, slots=True)
class InstanceConnection:
    """One configured Instance resolved with its Engine; credentials are never shown."""

    key: str
    name: str
    active: bool
    engine: str
    driver: str
    parameters: Mapping[str, Any]
    host: str | None
    port: int | None
    database: str
    username: str | None = field(repr=False)
    password: str | None = field(repr=False)
    options: Mapping[str, Any]
    path: Path | None


@dataclass(frozen=True, slots=True)
class QueryDefaults:
    """The resolved query defaults."""

    combination: FilterCombination
    limit: int
    order_field: str
    order_direction: OrderDirection


@dataclass(frozen=True, slots=True)
class InitialData:
    """The configured Initial Data records of one Entity."""

    entity: Any
    records: tuple[Mapping[str, Any], ...]


@dataclass(frozen=True, slots=True)
class Configuration:
    """The validated Database Configuration."""

    default_instance: database_instance
    instances: Mapping[str, InstanceConnection]
    storage_root: Path
    query: QueryDefaults
    after_generation_enabled: bool
    after_generation_fail_on_error: bool
    initial_data: tuple[InitialData, ...]


def _mapping(value: Any, where: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or not all(isinstance(key, str) for key in value):
        raise ConfigurationError(f"{where} must be a mapping")
    return value


def _text(value: Any, where: str, *, nullable: bool = False) -> Any:
    if value is None and nullable:
        return None
    if type(value) is not str or (not nullable and not value):
        raise ConfigurationError(f"{where} must be a non-empty string")
    return value


def _flag(value: Any, where: str) -> bool:
    if type(value) is not bool:
        raise ConfigurationError(f"{where} must be true or false")
    return value


def _member[E: Enum](enumeration: type[E], value: Any, where: str) -> E:
    members = enumeration.__members__
    if type(value) is not str or value not in members:
        raise ConfigurationError(f"{where} must be one of {', '.join(members)}")
    return members[value]


def _within(base: Path, relative: Any, where: str) -> Path:
    if type(relative) is not str or not relative or Path(relative).is_absolute():
        raise ConfigurationError(f"{where} must be a relative path")
    resolved = (base / relative).resolve()
    if not resolved.is_relative_to(base):
        raise ConfigurationError(f"{where} escapes its Database-owned directory")
    return resolved


def _instances(
    data: Mapping[str, Any], engines: Mapping[str, Any], storage_root: Path
) -> dict[str, InstanceConnection]:
    instances: dict[str, InstanceConnection] = {}
    names: set[str] = set()
    for key, value in _mapping(data, "instances").items():
        where = f"instances.{key}"
        entry = _mapping(value, where)
        if tuple(entry) != _INSTANCE_FIELDS:
            raise ConfigurationError(
                f"{where} must hold exactly {', '.join(_INSTANCE_FIELDS)} in that order"
            )
        name = _text(entry["name"], f"{where}.name")
        if name in names:
            raise ConfigurationError(f"{where}.name repeats another Instance name")
        names.add(name)
        engine_key = _text(entry["engine"], f"{where}.engine")
        if engine_key not in engines:
            raise ConfigurationError(f"{where}.engine names an undeclared Engine")
        engine = engines[engine_key]
        port = entry["port"]
        if port is not None and (type(port) is not int or port < 1):
            raise ConfigurationError(f"{where}.port must be a positive integer or null")
        active = _flag(entry["active"], f"{where}.active")
        connection = InstanceConnection(
            key=key,
            name=name,
            active=active,
            engine=engine_key,
            driver=engine["driver"],
            parameters=engine["parameters"],
            host=_text(entry["host"], f"{where}.host", nullable=True),
            port=port,
            database=_text(entry["database"], f"{where}.database"),
            username=_text(entry["username"], f"{where}.username", nullable=True),
            password=_text(entry["password"], f"{where}.password", nullable=True),
            options=_mapping(entry["options"], f"{where}.options"),
            path=(
                _within(storage_root, entry["database"], f"{where}.database")
                if engine["parameters"].get("storage") == "file"
                else None
            ),
        )
        if active:
            for required in engine["parameters"].get("required_parameters", ()):
                if required not in _INSTANCE_FIELDS or entry[required] in (None, ""):
                    raise ConfigurationError(
                        f"{where}.{required} is required by its Engine"
                    )
        instances[key] = connection
    return instances


def _parameters(parameters: Mapping[str, Any], where: str) -> None:
    unknown = sorted(set(parameters) - set(_ENGINE_PARAMETERS))
    if unknown:
        raise ConfigurationError(f"{where}.{unknown[0]} is not an Engine parameter")
    if parameters.get("storage") not in ("file", "server"):
        raise ConfigurationError(f"{where}.storage must be file or server")
    required = parameters.get("required_parameters")
    if not isinstance(required, list) or not all(
        item in _INSTANCE_FIELDS for item in required
    ):
        raise ConfigurationError(
            f"{where}.required_parameters must be a list of Instance fields"
        )
    if "foreign_keys" in parameters:
        _flag(parameters["foreign_keys"], f"{where}.foreign_keys")
    if "connect_arguments" in parameters:
        _mapping(parameters["connect_arguments"], f"{where}.connect_arguments")
    port = parameters.get("default_port")
    if "default_port" in parameters and (type(port) is not int or port < 1):
        raise ConfigurationError(f"{where}.default_port must be a positive integer")


def _engines(data: Any) -> dict[str, Mapping[str, Any]]:
    engines: dict[str, Mapping[str, Any]] = {}
    for key, value in _mapping(data, "engines").items():
        where = f"engines.{key}"
        entry = _mapping(value, where)
        if tuple(entry) != ("name", "driver", "parameters"):
            raise ConfigurationError(
                f"{where} must hold exactly name, driver, parameters"
            )
        _text(entry["name"], f"{where}.name")
        _text(entry["driver"], f"{where}.driver")
        parameters = _mapping(entry["parameters"], f"{where}.parameters")
        _parameters(parameters, f"{where}.parameters")
        engines[key] = entry
    return engines


def _query(data: Any) -> QueryDefaults:
    query = _mapping(data, "settings.query")
    order = _mapping(query.get("default_order"), "settings.query.default_order")
    limit = query.get("default_limit")
    if type(limit) is not int:
        raise ConfigurationError("settings.query.default_limit must be an integer")
    order_field = _text(order.get("field"), "settings.query.default_order.field")
    for item in entities:
        if order_field not in {field.name for field in item.declaration.fields}:
            raise ConfigurationError(
                "settings.query.default_order.field is not a Field of every Entity"
            )
    return QueryDefaults(
        combination=_member(
            FilterCombination,
            query.get("filter_combination"),
            "settings.query.filter_combination",
        ),
        limit=limit if limit > 0 else -1,
        order_field=order_field,
        order_direction=_member(
            OrderDirection,
            order.get("direction"),
            "settings.query.default_order.direction",
        ),
    )


def _initial_data(data: Any) -> tuple[InitialData, ...]:
    if not isinstance(data, list):
        raise ConfigurationError("initial_data must be a list")
    by_name = {item.declaration.name: item for item in entities}
    seen: set[str] = set()
    collection: list[InitialData] = []
    for index, value in enumerate(data):
        where = f"initial_data[{index}]"
        entry = _mapping(value, where)
        if tuple(entry) != ("entity", "records"):
            raise ConfigurationError(f"{where} must hold exactly entity and records")
        name = _text(entry["entity"], f"{where}.entity")
        if name not in by_name:
            raise ConfigurationError(
                f"{where}.entity names no Entity of the Entity Collection"
            )
        if name in seen:
            raise ConfigurationError(f"{where}.entity repeats {name}")
        seen.add(name)
        records = entry["records"]
        if not isinstance(records, list):
            raise ConfigurationError(f"{where}.records must be a list")
        collection.append(
            InitialData(
                entity=by_name[name],
                records=tuple(
                    _mapping(record, f"{where}.records[{position}]")
                    for position, record in enumerate(records)
                ),
            )
        )
    return tuple(collection)


def load(units: Collection[str]) -> Configuration:
    """Load and validate the Database Configuration for the Engine units that exist."""
    path = COMPONENT_ROOT / CONFIGURATION_FILE
    try:
        text = path.read_text(encoding="utf-8")
        data = yaml.safe_load(text)
    except OSError, yaml.YAMLError:
        failure = ConfigurationError(
            f"The Database Configuration {CONFIGURATION_FILE} is missing or unreadable "
            "beside the Database package"
        )
    else:
        failure = None
    # Raised outside the handler so no original error is attached.
    if failure is not None:
        raise failure
    content = _mapping(data, "The Database Configuration")
    if tuple(content) != _SECTIONS:
        raise ConfigurationError(
            f"The Database Configuration must hold exactly {', '.join(_SECTIONS)} in that order"
        )
    settings = _mapping(content["settings"], "settings")
    if tuple(settings) != ("default_instance", "storage_root", "query", "setup"):
        raise ConfigurationError(
            "settings must hold exactly default_instance, storage_root, query, setup"
        )
    storage_root = _within(
        COMPONENT_ROOT, settings.get("storage_root"), "settings.storage_root"
    )
    instances = _instances(
        content["instances"], _engines(content["engines"]), storage_root
    )

    members = {member.value for member in database_instance}
    unknown = sorted(members - instances.keys())
    if unknown:
        raise ConfigurationError(
            f"DatabaseInstance member {unknown[0]} names no configured Instance"
        )
    for key, instance in instances.items():
        if instance.active and key not in members:
            raise ConfigurationError(
                f"Active Instance {key} has no DatabaseInstance member; regenerate Database"
            )
        if instance.active and instance.engine not in units:
            raise ConfigurationError(
                f"Active Instance {key} uses Engine {instance.engine}, which has no Engine unit"
            )

    default_key = _text(settings["default_instance"], "settings.default_instance")
    if default_key not in instances or not instances[default_key].active:
        raise ConfigurationError(
            "settings.default_instance must name an active Instance"
        )

    setup = _mapping(settings.get("setup"), "settings.setup")
    after = _mapping(setup.get("after_generation"), "settings.setup.after_generation")
    if after.get("command") != "prepare":
        raise ConfigurationError(
            "settings.setup.after_generation.command must be prepare"
        )

    return Configuration(
        default_instance=database_instance(default_key),
        instances=instances,
        storage_root=storage_root,
        query=_query(settings.get("query")),
        after_generation_enabled=_flag(
            after.get("enabled"), "settings.setup.after_generation.enabled"
        ),
        after_generation_fail_on_error=_flag(
            after.get("fail_on_error"), "settings.setup.after_generation.fail_on_error"
        ),
        initial_data=_initial_data(content["initial_data"]),
    )
