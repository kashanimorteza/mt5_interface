"""The SQLite Engine unit: storage behavior shared by every Instance that uses SQLite."""

import decimal
import sqlite3
from collections.abc import Callable, Mapping, Sequence
from typing import Any, cast

from sqlalchemy import (
    URL,
    ColumnElement,
    Connection,
    Engine,
    Select,
    Table,
    and_,
    create_engine,
    delete,
    event,
    func,
    insert,
    or_,
    select,
    true,
    update,
)
from sqlalchemy.exc import SQLAlchemyError

from database.core.configuration import InstanceConnection
from database.core.errors import ConnectionFailureError, ExecutionError
from database.core.values import (
    CheckedFilter,
    CheckedOrder,
    FilterCombination,
    FilterOperator,
)

COLLATION = "exact_decimal"
"""Compares exact decimal text numerically."""

DECIMAL_SUM = "exact_decimal_sum"
"""Sums exact decimal text without rounding."""

_EXACT = decimal.Context(
    prec=decimal.MAX_PREC, Emax=decimal.MAX_EMAX, Emin=decimal.MIN_EMIN
)


def _compare_decimals(left: str, right: str) -> int:
    first, second = decimal.Decimal(left), decimal.Decimal(right)
    return (first > second) - (first < second)


class _DecimalSum:
    def __init__(self) -> None:
        self.total = decimal.Decimal(0)
        self.seen = False

    def step(self, value: Any) -> None:
        if value is not None:
            self.total = _EXACT.add(self.total, decimal.Decimal(str(value)))
            self.seen = True

    def finalize(self) -> str | None:
        return str(self.total) if self.seen else None


def create(connection: InstanceConnection) -> Engine:
    """Return the engine of one SQLite Instance, whose file lies beneath the storage root."""
    if connection.path is None:
        raise ConnectionFailureError(f"Instance {connection.key} has no file storage")
    try:
        connection.path.parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        failure = ConnectionFailureError(
            f"Could not prepare the storage directory of Instance {connection.key}"
        )
    else:
        failure = None
    if failure is not None:
        raise failure
    engine = create_engine(
        URL.create(connection.driver, database=str(connection.path)),
        connect_args=dict(connection.parameters.get("connect_arguments", {})),
    )
    foreign_keys = connection.parameters.get("foreign_keys") is True

    @event.listens_for(engine, "connect")
    def _prepare(dbapi_connection: sqlite3.Connection, _record: Any) -> None:
        # The driver leaves transactions to SQLAlchemy so DDL is transactional too.
        dbapi_connection.isolation_level = None
        if foreign_keys:
            dbapi_connection.execute("PRAGMA foreign_keys = ON")
        dbapi_connection.create_collation(COLLATION, _compare_decimals)
        # The stub types an aggregate's result as int only; SQLite accepts text.
        dbapi_connection.create_aggregate(DECIMAL_SUM, 1, cast(Any, _DecimalSum))

    @event.listens_for(engine, "begin")
    def _begin(connection: Connection) -> None:
        connection.exec_driver_sql("BEGIN")

    return engine


def _described(error: SQLAlchemyError) -> str:
    original = getattr(error, "orig", None)
    return str(original) if original is not None else type(error).__name__


def run[T](engine: Engine, key: str, work: Callable[[Connection], T]) -> T:
    """Run work in one transaction on the Instance, committing only when it completes."""
    try:
        connection = engine.connect()
    except SQLAlchemyError as error:
        failure: Exception | None = ConnectionFailureError(
            f"Could not connect to Instance {key}: {_described(error)}"
        )
    else:
        failure = None
    # Raised outside the handler so no original error, statement, or parameter is attached.
    if failure is not None:
        raise failure
    try:
        with connection.begin():
            result = work(connection)
    except SQLAlchemyError as error:
        failure = ExecutionError(
            f"Execution failed on Instance {key}: {_described(error)}"
        )
    else:
        return result
    finally:
        connection.close()
    raise failure


type Row = dict[str, Any]


def _column(table: Table, name: str, type_name: str) -> ColumnElement[Any]:
    column = table.c[name]
    return column.collate(COLLATION) if type_name == "decimal" else column


def _condition(table: Table, item: CheckedFilter) -> ColumnElement[bool]:
    raw = table.c[item.field]
    column = _column(table, item.field, item.type)
    value = item.value
    match item.operator:
        case FilterOperator.EQUALS:
            return column == value
        case FilterOperator.NOT_EQUALS:
            return column != value
        case FilterOperator.GREATER_THAN:
            return column > value
        case FilterOperator.GREATER_OR_EQUAL:
            return column >= value
        case FilterOperator.LESS_THAN:
            return column < value
        case FilterOperator.LESS_OR_EQUAL:
            return column <= value
        case FilterOperator.IN:
            return column.in_(value)
        case FilterOperator.CONTAINS:
            return func.instr(raw, value) > 0
        case FilterOperator.STARTS_WITH:
            return func.substr(raw, 1, len(value)) == value
        case FilterOperator.ENDS_WITH:
            return func.substr(raw, -len(value)) == value if value else raw.is_not(None)
        case FilterOperator.IS_NULL:
            return raw.is_(None)
        case FilterOperator.IS_NOT_NULL:
            return raw.is_not(None)


def _where(
    statement: Select[Any],
    table: Table,
    filters: Sequence[CheckedFilter],
    combination: FilterCombination,
) -> Select[Any]:
    if not filters:
        return statement
    conditions = [_condition(table, item) for item in filters]
    joined = and_ if combination is FilterCombination.AND else or_
    return statement.where(joined(*conditions))


def _rows(result: Any) -> list[Row]:
    return [dict(row) for row in result.mappings()]


def _one(result: Any) -> Row | None:
    row = result.mappings().one_or_none()
    return None if row is None else dict(row)


def insert_row(connection: Connection, table: Table, values: Mapping[str, Any]) -> Row:
    """Store one new record and return it as stored."""
    statement = insert(table).values(dict(values)).returning(*table.c)
    return dict(connection.execute(statement).mappings().one())


def update_row(
    connection: Connection, table: Table, key: Any, values: Mapping[str, Any]
) -> Row | None:
    """Replace the given values of the record with this id and return it, or None."""
    statement = (
        update(table).where(table.c.id == key).values(dict(values)).returning(*table.c)
    )
    return _one(connection.execute(statement))


def get_row(connection: Connection, table: Table, key: Any) -> Row | None:
    """Return the record with this id, or None."""
    return _one(connection.execute(select(table).where(table.c.id == key)))


def delete_row(connection: Connection, table: Table, key: Any) -> Row | None:
    """Delete the record with this id and return it as it was, or None."""
    statement = delete(table).where(table.c.id == key).returning(*table.c)
    return _one(connection.execute(statement))


def truncate(connection: Connection, table: Table) -> int:
    """Delete every record of the table, keeping the table, and return the deleted count."""
    return connection.execute(delete(table)).rowcount


def select_rows(
    connection: Connection,
    table: Table,
    filters: Sequence[CheckedFilter],
    combination: FilterCombination,
    orders: Sequence[CheckedOrder],
    limit: int,
) -> list[Row]:
    """Return the matching records in the given order, bounded by a positive limit."""
    statement = _where(select(table), table, filters, combination)
    for order in orders:
        column = _column(table, order.field, order.type)
        statement = statement.order_by(
            column.desc() if order.descending else column.asc()
        )
    if limit > 0:
        statement = statement.limit(limit)
    return _rows(connection.execute(statement))


def count(
    connection: Connection,
    table: Table,
    filters: Sequence[CheckedFilter],
    combination: FilterCombination,
) -> int:
    """Return the number of matching records."""
    statement = _where(
        select(func.count()).select_from(table), table, filters, combination
    )
    return connection.execute(statement).scalar_one()


def aggregate(
    connection: Connection,
    table: Table,
    function: str,
    field: str,
    type_name: str,
    filters: Sequence[CheckedFilter],
    combination: FilterCombination,
) -> Any:
    """Return the sum, minimum, or maximum of one Field over matching records, ignoring nulls."""
    raw = table.c[field]
    if function == "sum":
        value: ColumnElement[Any] = (
            getattr(func, DECIMAL_SUM)(raw, type_=raw.type)
            if type_name == "decimal"
            else func.sum(raw)
        )
    else:
        value = getattr(func, function)(_column(table, field, type_name))
    statement = _where(select(value).select_from(table), table, filters, combination)
    return connection.execute(statement).scalar_one()


def matching_rows(
    connection: Connection, table: Table, values: Mapping[str, tuple[str, Any]]
) -> list[Row]:
    """Return the records equal to every given value, each given with its declared Type."""
    conditions = [
        table.c[name].is_(None)
        if value is None
        else _column(table, name, type_name) == value
        for name, (type_name, value) in values.items()
    ]
    statement = select(table).where(and_(true(), *conditions)).order_by(table.c.id)
    return _rows(connection.execute(statement))


def execute(
    connection: Connection,
    command: str,
    parameters: Mapping[str, Any] | tuple[Any, ...],
) -> tuple[tuple[Row, ...] | None, int | None, tuple[str, ...] | None]:
    """Run one native command with bound parameters and return rows, affected, and columns."""
    result = connection.exec_driver_sql(command, parameters)
    if result.returns_rows:
        columns = tuple(result.keys())
        return tuple(dict(row) for row in result.mappings()), None, columns
    return None, (result.rowcount if result.rowcount >= 0 else None), None
