"""Symbols Adapter of MT5 Group: one Endpoint for every Function of the Symbols group."""

from typing import Annotated

from fastapi import APIRouter, Body
from logic.interface import MT5
from pydantic import JsonValue

from api.endpoints import PlainRoute

router = APIRouter(prefix="/symbols", tags=["MT5 · Symbols"], route_class=PlainRoute)


@router.post(
    "/symbols_total",
    openapi_extra={
        "externalDocs": {
            "description": "symbols_total in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5symbolstotal_py",
        }
    },
)
def symbols_total(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
) -> JsonValue:
    """Return the number of all financial instruments."""
    return MT5(terminal).Symbols.symbols_total()


@router.post(
    "/symbols_get",
    openapi_extra={
        "externalDocs": {
            "description": "symbols_get in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5symbolsget_py",
        }
    },
)
def symbols_get(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
    group: Annotated[
        str | None,
        Body(
            embed=True,
            description="Filter on symbol names, such as *USD*; several patterns are separated by commas and ! excludes.",
            examples=["*USD*"],
        ),
    ] = None,
) -> JsonValue:
    """Return all financial instruments, optionally filtered by group."""
    return MT5(terminal).Symbols.symbols_get(group=group)


@router.post(
    "/symbol_info",
    openapi_extra={
        "externalDocs": {
            "description": "symbol_info in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5symbolinfo_py",
        }
    },
)
def symbol_info(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
    symbol: Annotated[
        str,
        Body(
            embed=True,
            description="Financial instrument name, such as EURUSD.",
            examples=["EURUSD"],
        ),
    ],
) -> JsonValue:
    """Return data on a financial instrument."""
    return MT5(terminal).Symbols.symbol_info(symbol=symbol)


@router.post(
    "/symbol_info_tick",
    openapi_extra={
        "externalDocs": {
            "description": "symbol_info_tick in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5symbolinfotick_py",
        }
    },
)
def symbol_info_tick(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
    symbol: Annotated[
        str,
        Body(
            embed=True,
            description="Financial instrument name, such as EURUSD.",
            examples=["EURUSD"],
        ),
    ],
) -> JsonValue:
    """Return the last tick of a financial instrument."""
    return MT5(terminal).Symbols.symbol_info_tick(symbol=symbol)


@router.post(
    "/symbol_select",
    openapi_extra={
        "externalDocs": {
            "description": "symbol_select in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5symbolselect_py",
        }
    },
)
def symbol_select(
    terminal: Annotated[
        str,
        Body(
            embed=True,
            description="Name of a Terminal in MT5 Service's config.yaml, such as demo.",
            examples=["demo"],
        ),
    ],
    symbol: Annotated[
        str,
        Body(
            embed=True,
            description="Financial instrument name, such as EURUSD.",
            examples=["EURUSD"],
        ),
    ],
    enable: Annotated[
        bool | None,
        Body(
            embed=True,
            description="true or left out selects the symbol in Market Watch; false removes it.",
            examples=[True],
        ),
    ] = None,
) -> JsonValue:
    """Select a symbol in MarketWatch, or remove it when enable is False."""
    return MT5(terminal).Symbols.symbol_select(symbol=symbol, enable=enable)
