"""Validation: the shared private behavior every Entity runs on top of the modeling package."""

from contextvars import ContextVar
from typing import Any, ClassVar, LiteralString, Self, cast

from pydantic import ValidationError
from pydantic_core import InitErrorDetails, PydanticCustomError
from sqlmodel import SQLModel
from sqlmodel.main import SQLModelConfig

from entity.core import _storage, _types
from entity.core.declaration import Declaration, FieldDeclaration, ValueGeneration

REPLACEMENT = "**********"
"""What a marked Field's input is replaced with in every validation message."""

_initializing: ContextVar[bool] = ContextVar("_initializing", default=False)
_stored: ContextVar[bool] = ContextVar("_stored", default=False)


def _is_auto_increment(field: FieldDeclaration) -> bool:
    return field.value_generation is ValueGeneration.AUTO_INCREMENT


class Base(SQLModel, registry=_storage.registry):
    """Strict construction and assignment validation shared by every Entity."""

    model_config = SQLModelConfig(strict=True, extra="forbid", validate_default=True)

    declaration: ClassVar[Declaration]

    __hash__ = None

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        if "declaration" not in cls.__dict__:
            return
        declaration = cls.declaration
        where = f"Entity {declaration.name!r}"
        if cls.__name__ != _storage.type_name(declaration.name):
            raise TypeError(f"{where} type name does not match its physical name")
        if cls.__dict__.get("__tablename__") != _storage.table_name(declaration.name):
            raise TypeError(f"{where} table name does not match its physical name")
        if list(cls.model_fields) != [field.name for field in declaration.fields]:
            raise TypeError(f"{where} Fields do not match its Declaration")
        annotations = cls.__annotations__
        for field in declaration.fields:
            optional = field.nullable or _is_auto_increment(field)
            if annotations.get(field.name) != _types.python_type(
                field.type, optional=optional
            ):
                raise TypeError(f"{where} Field {field.name!r} does not match its Type")

    @classmethod
    def _sensitive(cls) -> set[str]:
        return {
            field.name
            for field in cls.declaration.fields
            if field.sensitivity is not None
        }

    @classmethod
    def _masked(cls, error: ValidationError) -> ValidationError:
        sensitive = cls._sensitive()
        details: list[InitErrorDetails] = []
        for item in error.errors():
            value = item["input"]
            if item["loc"] and item["loc"][0] in sensitive:
                value = REPLACEMENT
            elif isinstance(value, dict):
                value = {
                    k: REPLACEMENT if k in sensitive else v for k, v in value.items()
                }
            details.append(
                {
                    "type": PydanticCustomError(
                        cast(LiteralString, item["type"]),
                        cast(LiteralString, item["msg"]),
                    ),
                    "loc": item["loc"],
                    "input": value,
                }
            )
        return ValidationError.from_exception_data(cls.__name__, details)

    @classmethod
    def _refused(
        cls, name: str, kind: str, message: str, value: Any
    ) -> ValidationError:
        shown = REPLACEMENT if name in cls._sensitive() else value
        return ValidationError.from_exception_data(
            cls.__name__,
            [
                {
                    "type": PydanticCustomError(
                        cast(LiteralString, kind), cast(LiteralString, message)
                    ),
                    "loc": (name,),
                    "input": shown,
                }
            ],
        )

    @classmethod
    def model_validate(
        cls,
        obj: Any,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: dict[str, Any] | None = None,
        update: dict[str, Any] | None = None,
    ) -> Self:
        token = _initializing.set(True)
        try:
            return super().model_validate(
                obj,
                strict=strict,
                from_attributes=from_attributes,
                context=context,
                update=update,
            )
        except ValidationError as error:
            raise cls._masked(error) from None
        finally:
            _initializing.reset(token)

    @classmethod
    def _from_stored(cls, data: dict[str, Any]) -> Self:
        token = _stored.set(True)
        try:
            return cls(**data)
        finally:
            _stored.reset(token)

    def __init__(self, **data: Any) -> None:
        if _initializing.get():
            super().__init__(**data)
            return
        cls = type(self)
        if not _stored.get():
            for field in cls.declaration.fields:
                if _is_auto_increment(field) and field.name in data:
                    raise cls._refused(
                        field.name,
                        "auto_increment",
                        "Value is assigned by storage",
                        data[field.name],
                    )
        validated = cls.model_validate(data)
        token = _initializing.set(True)
        try:
            super().__init__(
                **{name: validated.__dict__[name] for name in cls.model_fields}
            )
        finally:
            _initializing.reset(token)
        object.__setattr__(
            self, "__pydantic_fields_set__", set(validated.model_fields_set)
        )

    def __setattr__(self, name: str, value: Any) -> None:
        cls = type(self)
        if _initializing.get() or name not in cls.model_fields:
            super().__setattr__(name, value)
            return
        field = next(item for item in cls.declaration.fields if item.name == name)
        if field.immutable or _is_auto_increment(field):
            raise cls._refused(name, "frozen_field", "Field is frozen", value)
        data = {key: getattr(self, key) for key in cls.model_fields}
        data[name] = value
        validated = cls.model_validate(data)
        token = _initializing.set(True)
        try:
            super().__setattr__(name, validated.__dict__[name])
        finally:
            _initializing.reset(token)
