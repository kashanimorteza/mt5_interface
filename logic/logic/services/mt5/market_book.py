"""MarketBook Function Group of MT5 Service."""

from logic.services.mt5.terminal import JSON, call


class MarketBook:
    """Subscribe to, read, and release Market Depth."""

    def __init__(self, terminal: str) -> None:
        """Bind this Function Group to the Terminal of its MT5 instance."""
        self._terminal = terminal

    def market_book_add(self, symbol: str) -> JSON:
        """Subscribe to Market Depth change events for a symbol."""
        return call(self._terminal, "market_book_add", {"symbol": symbol})

    def market_book_get(self, symbol: str) -> JSON:
        """Return the Market Depth entries of a symbol."""
        return call(self._terminal, "market_book_get", {"symbol": symbol})

    def market_book_release(self, symbol: str) -> JSON:
        """Cancel the Market Depth subscription of a symbol."""
        return call(self._terminal, "market_book_release", {"symbol": symbol})
