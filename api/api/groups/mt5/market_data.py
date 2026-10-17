"""MarketData Adapter of MT5 Group: one Endpoint for every Function of the MarketData group."""

from typing import Annotated

from fastapi import APIRouter, Body
from logic.interface import MT5
from pydantic import JsonValue

from api.endpoints import PlainRoute

router = APIRouter(
    prefix="/market_data", tags=["MT5 · MarketData"], route_class=PlainRoute
)


@router.post(
    "/copy_rates_from",
    openapi_extra={
        "externalDocs": {
            "description": "copy_rates_from in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5copyratesfrom_py",
        }
    },
)
def copy_rates_from(
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
    timeframe: Annotated[
        int,
        Body(
            embed=True,
            description="Timeframe as a TIMEFRAME_* value from the Constants Endpoint, such as 16385 for TIMEFRAME_H1.",
            examples=[16385],
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
    count: Annotated[
        int, Body(embed=True, description="Number of items to return.", examples=[10])
    ],
) -> JsonValue:
    """Return bars starting from a date."""
    return MT5(terminal).MarketData.copy_rates_from(
        symbol=symbol, timeframe=timeframe, date_from=date_from, count=count
    )


@router.post(
    "/copy_rates_from_pos",
    openapi_extra={
        "externalDocs": {
            "description": "copy_rates_from_pos in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5copyratesfrompos_py",
        }
    },
)
def copy_rates_from_pos(
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
    timeframe: Annotated[
        int,
        Body(
            embed=True,
            description="Timeframe as a TIMEFRAME_* value from the Constants Endpoint, such as 16385 for TIMEFRAME_H1.",
            examples=[16385],
        ),
    ],
    start_pos: Annotated[
        int,
        Body(
            embed=True,
            description="Index of the first bar, counted from the current bar, which is 0.",
            examples=[0],
        ),
    ],
    count: Annotated[
        int, Body(embed=True, description="Number of items to return.", examples=[10])
    ],
) -> JsonValue:
    """Return bars starting from a bar index."""
    return MT5(terminal).MarketData.copy_rates_from_pos(
        symbol=symbol, timeframe=timeframe, start_pos=start_pos, count=count
    )


@router.post(
    "/copy_rates_range",
    openapi_extra={
        "externalDocs": {
            "description": "copy_rates_range in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5copyratesrange_py",
        }
    },
)
def copy_rates_range(
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
    timeframe: Annotated[
        int,
        Body(
            embed=True,
            description="Timeframe as a TIMEFRAME_* value from the Constants Endpoint, such as 16385 for TIMEFRAME_H1.",
            examples=[16385],
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
    """Return bars within a date range."""
    return MT5(terminal).MarketData.copy_rates_range(
        symbol=symbol, timeframe=timeframe, date_from=date_from, date_to=date_to
    )


@router.post(
    "/copy_ticks_from",
    openapi_extra={
        "externalDocs": {
            "description": "copy_ticks_from in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5copyticksfrom_py",
        }
    },
)
def copy_ticks_from(
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
    date_from: Annotated[
        int,
        Body(
            embed=True,
            description="Start date as a Timestamp, whole seconds since 1970-01-01 UTC.",
            examples=[1704067200],
        ),
    ],
    count: Annotated[
        int, Body(embed=True, description="Number of items to return.", examples=[10])
    ],
    flags: Annotated[
        int,
        Body(
            embed=True,
            description="Tick type as a COPY_TICKS_* value from the Constants Endpoint, such as -1 for COPY_TICKS_ALL.",
            examples=[-1],
        ),
    ],
) -> JsonValue:
    """Return ticks starting from a date."""
    return MT5(terminal).MarketData.copy_ticks_from(
        symbol=symbol, date_from=date_from, count=count, flags=flags
    )


@router.post(
    "/copy_ticks_range",
    openapi_extra={
        "externalDocs": {
            "description": "copy_ticks_range in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5copyticksrange_py",
        }
    },
)
def copy_ticks_range(
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
    flags: Annotated[
        int,
        Body(
            embed=True,
            description="Tick type as a COPY_TICKS_* value from the Constants Endpoint, such as -1 for COPY_TICKS_ALL.",
            examples=[-1],
        ),
    ],
) -> JsonValue:
    """Return ticks within a date range."""
    return MT5(terminal).MarketData.copy_ticks_range(
        symbol=symbol, date_from=date_from, date_to=date_to, flags=flags
    )
