"""MarketBook Adapter of MT5 Group: one Endpoint for every Function of the MarketBook group."""

from typing import Annotated

from fastapi import APIRouter, Body
from logic.interface import MT5
from pydantic import JsonValue

from api.endpoints import PlainRoute

router = APIRouter(
    prefix="/market_book", tags=["MT5 · MarketBook"], route_class=PlainRoute
)


@router.post(
    "/market_book_add",
    openapi_extra={
        "externalDocs": {
            "description": "market_book_add in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5marketbookadd_py",
        }
    },
)
def market_book_add(
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
    """Subscribe to Market Depth change events for a symbol."""
    return MT5(terminal).MarketBook.market_book_add(symbol=symbol)


@router.post(
    "/market_book_get",
    openapi_extra={
        "externalDocs": {
            "description": "market_book_get in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5marketbookget_py",
        }
    },
)
def market_book_get(
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
    """Return the Market Depth entries of a symbol."""
    return MT5(terminal).MarketBook.market_book_get(symbol=symbol)


@router.post(
    "/market_book_release",
    openapi_extra={
        "externalDocs": {
            "description": "market_book_release in the MetaTrader 5 Python documentation",
            "url": "https://www.mql5.com/en/docs/python_metatrader5/mt5marketbookrelease_py",
        }
    },
)
def market_book_release(
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
    """Cancel the Market Depth subscription of a symbol."""
    return MT5(terminal).MarketBook.market_book_release(symbol=symbol)
