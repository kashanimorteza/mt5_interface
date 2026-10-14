"""The market_book Adapter: one Endpoint for every Function of the MarketBook Function Group."""

from typing import Annotated, Any

from fastapi import APIRouter, Body
from logic.interface import MT5

from api import endpoints

router = APIRouter(
    prefix="/market_book",
    tags=["MT5 · market_book"],
    route_class=endpoints.ResultRoute,
)


@router.post("/market_book_add", response_model=None)
def market_book_add(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
) -> Any:
    """Subscribes the MetaTrader 5 terminal to the Market Depth change events for a specified symbol."""
    return MT5.MarketBook.market_book_add(terminal, symbol)


@router.post("/market_book_get", response_model=None)
def market_book_get(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
) -> Any:
    """Returns a tuple from BookInfo featuring Market Depth entries for the specified symbol."""
    return MT5.MarketBook.market_book_get(terminal, symbol)


@router.post("/market_book_release", response_model=None)
def market_book_release(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
) -> Any:
    """Cancels subscription of the MetaTrader 5 terminal to the Market Depth change events for a specified symbol."""
    return MT5.MarketBook.market_book_release(terminal, symbol)
