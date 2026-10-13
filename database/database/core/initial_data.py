"""insert_initial_data: the configured Initial Data, inserted repeatably and unchanged."""

import json
from typing import Any

from pydantic import ValidationError
from sqlalchemy import Connection

from database.core import data
from database.core.errors import ConfigurationError, ExecutionError
from database.core.values import SetupResult, database_instance


def _built(entity: Any, position: int, record: Any) -> Any:
    try:
        return entity.from_json(json.dumps(record, ensure_ascii=False))
    except (ValidationError, TypeError, ValueError) as error:
        names = (
            sorted({str(item["loc"][0]) for item in error.errors() if item["loc"]})
            if isinstance(error, ValidationError)
            else []
        )
        failure = ConfigurationError(
            f"Initial Data record {position} of {entity.declaration.name} does not satisfy "
            f"its Entity contract in: {', '.join(names) or 'the record'}"
        )
    # Raised outside the handler so no record value is attached.
    raise failure


def _prepared() -> list[tuple[Any, int, dict[str, Any], dict[str, tuple[str, Any]]]]:
    prepared = []
    for group in data.configuration().initial_data:
        entity = group.entity
        for position, record in enumerate(group.records):
            built = _built(entity, position, record)
            values: dict[str, Any] = {}
            compared: dict[str, tuple[str, Any]] = {}
            for field in entity.declaration.fields:
                value = getattr(built, field.name)
                if field.value_generation is not None and field.name not in record:
                    if value is not None:
                        values[field.name] = value
                    continue
                values[field.name] = value
                compared[field.name] = (str(field.type), value)
            prepared.append((entity, position, values, compared))
    return prepared


def insert(unit: Any, link: Connection) -> tuple[int, int]:
    """Insert every missing configured record and skip identical ones; return both counts."""
    inserted = skipped = 0
    for entity, position, values, compared in _prepared():
        table = entity.__table__
        if unit.matching_rows(link, table, compared):
            skipped += 1
            continue
        for constraint in entity.declaration.unique_constraints:
            if any(
                compared.get(name, (None, None))[1] is None
                for name in constraint.fields
            ):
                continue
            key = {name: compared[name] for name in constraint.fields}
            if unit.matching_rows(link, table, key):
                raise ExecutionError(
                    f"Initial Data record {position} of {entity.declaration.name} conflicts "
                    f"with a stored record on ({', '.join(constraint.fields)}); nothing was inserted"
                )
        unit.insert_row(link, table, values)
        inserted += 1
    return inserted, skipped


def insert_initial_data(instance: database_instance | None) -> SetupResult:
    """Insert the configured Initial Data on the selected Instance in one transaction."""
    (inserted, skipped), used = data.run(instance, insert)
    return SetupResult(
        command="insert_initial_data",
        instance=used,
        success=True,
        affected=inserted + skipped,
        message=f"{inserted} Initial Data records inserted, {skipped} already present.",
    )
