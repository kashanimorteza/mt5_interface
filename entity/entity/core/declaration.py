"""The public Declaration contract: the structured meaning of every Entity and Field."""

from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Final, final

from entity.core import _types


class FieldType(StrEnum):
    """The closed set of Field Types."""

    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    DECIMAL = "decimal"
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    DATE = "date"
    TIME = "time"
    UUID = "uuid"


class ValueGeneration(StrEnum):
    """The declared ways a Field value is supplied automatically."""

    AUTO_INCREMENT = "auto_increment"
    GENERATED_IDENTIFIER = "generated_identifier"


class Sensitivity(StrEnum):
    """The recognized Sensitivity Markers."""

    PASSWORD = "password"
    SENSITIVE = "sensitive"


@final
class NoDefault:
    """The type of NO_DEFAULT, which marks a Field Declaration with no Default Value."""

    _instance: NoDefault | None = None

    def __new__(cls) -> NoDefault:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self) -> str:
        return "NO_DEFAULT"


NO_DEFAULT: Final = NoDefault()
"""An absent Default Value, distinct from an explicit null default."""


def _tuple_of[T](values: Sequence[T], what: str) -> tuple[T, ...]:
    if isinstance(values, str) or not isinstance(values, Sequence):
        raise TypeError(f"{what} must be an ordered sequence")
    return tuple(values)


def _field_names(fields: Sequence[str], what: str) -> tuple[str, ...]:
    names = _tuple_of(fields, what)
    if not names:
        raise ValueError(f"{what} must name at least one Field")
    if len(set(names)) != len(names):
        raise ValueError(f"{what} repeats a Field")
    return names


@dataclass(frozen=True, slots=True)
class FieldConstraints:
    """The value constraints of one Field."""

    size: int | None = None

    def __post_init__(self) -> None:
        if self.size is not None and (type(self.size) is not int or self.size < 1):
            raise ValueError("size must be a positive length")


@dataclass(frozen=True, slots=True)
class Relation:
    """Entity Metadata connecting one local Field to a target Entity and target Field by logical name."""

    local_field: str
    target_entity: str
    target_field: str


@dataclass(frozen=True, slots=True)
class UniquenessConstraint:
    """Entity Metadata requiring one Field or an ordered combination of Fields to be unique."""

    fields: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "fields", _field_names(self.fields, "A Uniqueness Constraint")
        )


@dataclass(frozen=True, slots=True)
class Index:
    """Entity Metadata recording an access intention for one Field or an ordered combination of Fields."""

    fields: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "fields", _field_names(self.fields, "An Index"))


@dataclass(frozen=True, slots=True)
class FieldDeclaration:
    """The complete structured public record of one Field."""

    name: str
    type: FieldType
    nullable: bool
    description: str | None = None
    default: Any = NO_DEFAULT
    sensitivity: Sensitivity | None = None
    immutable: bool = False
    constraints: FieldConstraints = field(default_factory=FieldConstraints)
    value_generation: ValueGeneration | None = None

    def __post_init__(self) -> None:
        where = f"Field {self.name!r}"
        if type(self.name) is not str or not self.name:
            raise ValueError("A Field name must be a non-empty string")
        if not isinstance(self.type, FieldType) or not _types.is_known(self.type):
            raise ValueError(f"{where} has an unknown Type")
        if type(self.nullable) is not bool or type(self.immutable) is not bool:
            raise ValueError(f"{where} must state nullable and immutable as booleans")
        if self.sensitivity is not None and not isinstance(
            self.sensitivity, Sensitivity
        ):
            raise ValueError(f"{where} has an unrecognized Sensitivity Marker")
        if not isinstance(self.constraints, FieldConstraints):
            raise TypeError(f"{where} has invalid constraints")
        if self.constraints.size is not None and self.type is not FieldType.STRING:
            raise ValueError(f"{where} has a size but is not a string")
        if self.value_generation is not None:
            if not isinstance(self.value_generation, ValueGeneration):
                raise ValueError(f"{where} has an unknown Value Generation")
            if self.default is not NO_DEFAULT:
                raise ValueError(
                    f"{where} has both a Default Value and Value Generation"
                )
            if (
                self.value_generation is ValueGeneration.AUTO_INCREMENT
                and self.type is not FieldType.INTEGER
            ):
                raise ValueError(f"{where} uses auto_increment but is not an integer")
            if (
                self.value_generation is ValueGeneration.GENERATED_IDENTIFIER
                and self.type not in {FieldType.UUID, FieldType.STRING}
            ):
                raise ValueError(
                    f"{where} uses generated_identifier but is not a uuid or string"
                )
        if self.default is not NO_DEFAULT:
            if self.default is None:
                if not self.nullable:
                    raise ValueError(f"{where} has a null default but is not nullable")
            elif not _types.matches(self.type, self.default):
                raise ValueError(f"{where} has a default that does not match its Type")
            elif (
                self.constraints.size is not None
                and len(self.default) > self.constraints.size
            ):
                raise ValueError(f"{where} has a default longer than its size")


@dataclass(frozen=True, slots=True)
class Declaration:
    """The complete structured public record of one Entity."""

    name: str
    description: str | None
    fields: tuple[FieldDeclaration, ...]
    primary_key: str = "id"
    relations: tuple[Relation, ...] = ()
    unique_constraints: tuple[UniquenessConstraint, ...] = ()
    indexes: tuple[Index, ...] = ()

    def __post_init__(self) -> None:
        if type(self.name) is not str or not self.name:
            raise ValueError("An Entity name must be a non-empty string")
        where = f"Entity {self.name!r}"
        for member in ("fields", "relations", "unique_constraints", "indexes"):
            object.__setattr__(
                self, member, _tuple_of(getattr(self, member), f"{where} {member}")
            )
        if not all(isinstance(item, FieldDeclaration) for item in self.fields):
            raise TypeError(f"{where} fields must be Field Declarations")
        names = [item.name for item in self.fields]
        if len(set(names)) != len(names):
            raise ValueError(f"{where} repeats a Field name")
        by_name = {item.name: item for item in self.fields}

        identity = by_name.get(self.primary_key)
        if self.primary_key != "id" or identity is None:
            raise ValueError(f"{where} must name id as its Primary Key")
        if identity.nullable or not identity.immutable:
            raise ValueError(f"{where} id must be non-nullable and immutable")
        activity = by_name.get("is_active")
        if (
            activity is None
            or activity.type is not FieldType.BOOLEAN
            or activity.nullable
            or activity.immutable
        ):
            raise ValueError(
                f"{where} is_active must be a non-nullable, mutable boolean"
            )

        local_fields: set[str] = set()
        for relation in self.relations:
            if not isinstance(relation, Relation):
                raise TypeError(f"{where} relations must be Relations")
            if relation.local_field not in by_name:
                raise ValueError(
                    f"{where} Relation names unknown Field {relation.local_field!r}"
                )
            if relation.local_field in local_fields:
                raise ValueError(
                    f"{where} has more than one Relation on {relation.local_field!r}"
                )
            local_fields.add(relation.local_field)

        for member, kind in (
            ("unique_constraints", UniquenessConstraint),
            ("indexes", Index),
        ):
            entries = getattr(self, member)
            if not all(isinstance(entry, kind) for entry in entries):
                raise TypeError(f"{where} {member} must be {kind.__name__} entries")
            if len({entry.fields for entry in entries}) != len(entries):
                raise ValueError(f"{where} {member} repeats an entry")
            for entry in entries:
                unknown = [name for name in entry.fields if name not in by_name]
                if unknown:
                    raise ValueError(
                        f"{where} {member} names unknown Field {unknown[0]!r}"
                    )
