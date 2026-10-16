"""MarketBook Function Group of MT5 Service."""

from logic.services.mt5.terminal import JSON, call


class MarketBook:
    """Subscribe to, read, and release Market Depth."""

    @staticmethod
    def market_book_add(terminal: str, symbol: str) -> JSON:
        """Subscribe to Market Depth change events for a symbol."""
        return call(terminal, "market_book_add", {"symbol": symbol})

    @staticmethod
    def market_book_get(terminal: str, symbol: str) -> JSON:
        """Return the Market Depth entries of a symbol."""
        return call(terminal, "market_book_get", {"symbol": symbol})

    @staticmethod
    def market_book_release(terminal: str, symbol: str) -> JSON:
        """Cancel the Market Depth subscription of a symbol."""
        return call(terminal, "market_book_release", {"symbol": symbol})
