"""History Adapter of MT5 Group: one Endpoint for every Function of the History group."""

from typing import Annotated

from fastapi import APIRouter, Body
from logic.interface import MT5
from pydantic import JsonValue

from api.endpoints import PlainRoute

router = APIRouter(prefix="/history", tags=["MT5 · History"], route_class=PlainRoute)


@router.post(
    "/history_orders_total",
    openapi_extra={
        "externalDocs": {
            "description": "history_orders_total in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5historyorderstotal_py",
        }
    },
)
def history_orders_total(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
    date_from: Annotated[
        int,
        Body(
            embed=True,
            description="Start date as a Timestamp, whole seconds since 1970-01-01 UTC.",
            examples=[1704067200],
        ),
    ],
    date_to: Annotated[
        int,
        Body(
            embed=True,
            description="End date as a Timestamp, whole seconds since 1970-01-01 UTC.",
            examples=[1704153600],
        ),
    ],
) -> JsonValue:
    """Return the number of history orders within an interval."""
    return MT5(terminal).History.history_orders_total(
        date_from=date_from, date_to=date_to
    )


@router.post(
    "/history_orders_get",
    openapi_extra={
        "externalDocs": {
            "description": "history_orders_get in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5historyordersget_py",
        }
    },
)
def history_orders_get(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
    date_from: Annotated[
        int | None,
        Body(
            embed=True,
            description="Start date as a Timestamp, whole seconds since 1970-01-01 UTC.",
            examples=[1704067200],
        ),
    ] = None,
    date_to: Annotated[
        int | None,
        Body(
            embed=True,
            description="End date as a Timestamp, whole seconds since 1970-01-01 UTC.",
            examples=[1704153600],
        ),
    ] = None,
    group: Annotated[
        str | None,
        Body(
            embed=True,
            description="Filter on symbol names, such as *USD*; several patterns are separated by commas and ! excludes.",
            examples=["*USD*"],
        ),
    ] = None,
    ticket: Annotated[
        int | None,
        Body(
            embed=True,
            description="Ticket of one order, position, or deal.",
            examples=[530218319],
        ),
    ] = None,
    position: Annotated[
        int | None,
        Body(
            embed=True,
            description="Ticket of the position the orders or deals belong to.",
            examples=[530218319],
        ),
    ] = None,
) -> JsonValue:
    """Return history orders within an interval, or by order or position ticket."""
    return MT5(terminal).History.history_orders_get(
        date_from=date_from,
        date_to=date_to,
        group=group,
        ticket=ticket,
        position=position,
    )


@router.post(
    "/history_deals_total",
    openapi_extra={
        "externalDocs": {
            "description": "history_deals_total in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5historydealstotal_py",
        }
    },
)
def history_deals_total(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
    date_from: Annotated[
        int,
        Body(
            embed=True,
            description="Start date as a Timestamp, whole seconds since 1970-01-01 UTC.",
            examples=[1704067200],
        ),
    ],
    date_to: Annotated[
        int,
        Body(
            embed=True,
            description="End date as a Timestamp, whole seconds since 1970-01-01 UTC.",
            examples=[1704153600],
        ),
    ],
) -> JsonValue:
    """Return the number of history deals within an interval."""
    return MT5(terminal).History.history_deals_total(
        date_from=date_from, date_to=date_to
    )


@router.post(
    "/history_deals_get",
    openapi_extra={
        "externalDocs": {
            "description": "history_deals_get in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5historydealsget_py",
        }
    },
)
def history_deals_get(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
    date_from: Annotated[
        int | None,
        Body(
            embed=True,
            description="Start date as a Timestamp, whole seconds since 1970-01-01 UTC.",
            examples=[1704067200],
        ),
    ] = None,
    date_to: Annotated[
        int | None,
        Body(
            embed=True,
            description="End date as a Timestamp, whole seconds since 1970-01-01 UTC.",
            examples=[1704153600],
        ),
    ] = None,
    group: Annotated[
        str | None,
        Body(
            embed=True,
            description="Filter on symbol names, such as *USD*; several patterns are separated by commas and ! excludes.",
            examples=["*USD*"],
        ),
    ] = None,
    ticket: Annotated[
        int | None,
        Body(
            embed=True,
            description="Ticket of one order, position, or deal.",
            examples=[530218319],
        ),
    ] = None,
    position: Annotated[
        int | None,
        Body(
            embed=True,
            description="Ticket of the position the orders or deals belong to.",
            examples=[530218319],
        ),
    ] = None,
) -> JsonValue:
    """Return history deals within an interval, or by order or position ticket."""
    return MT5(terminal).History.history_deals_get(
        date_from=date_from,
        date_to=date_to,
        group=group,
        ticket=ticket,
        position=position,
    )
