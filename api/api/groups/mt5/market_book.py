"""MarketBook Adapter of MT5 Group: one Endpoint for every Function of the MarketBook group."""

from typing import Annotated

from fastapi import APIRouter, Body
from logic.interface import MT5
from pydantic import JsonValue

router = APIRouter(prefix="/market_book", tags=["MT5 · MarketBook"])


@router.post("/market_book_add")
def market_book_add(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
) -> JsonValue:
    """Subscribe to Market Depth change events for a symbol."""
    return MT5.MT5(terminal).MarketBook.market_book_add(symbol=symbol)


@router.post("/market_book_get")
def market_book_get(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
) -> JsonValue:
    """Return the Market Depth entries of a symbol."""
    return MT5.MT5(terminal).MarketBook.market_book_get(symbol=symbol)


@router.post("/market_book_release")
def market_book_release(
    terminal: Annotated[str, Body(embed=True)],
    symbol: Annotated[str, Body(embed=True)],
) -> JsonValue:
    """Cancel the Market Depth subscription of a symbol."""
    return MT5.MT5(terminal).MarketBook.market_book_release(symbol=symbol)
