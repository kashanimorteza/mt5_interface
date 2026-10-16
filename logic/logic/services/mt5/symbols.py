"""Symbols Function Group of MT5 Service."""

from logic.services.mt5.terminal import JSON, call


class Symbols:
    """Count, list, inspect, and select financial instruments."""

    def __init__(self, terminal: str) -> None:
        """Bind this Function Group to the Terminal of its MT5 instance."""
        self._terminal = terminal

    def symbols_total(self) -> JSON:
        """Return the number of all financial instruments."""
        return call(self._terminal, "symbols_total")

    def symbols_get(self, group: str | None = None) -> JSON:
        """Return all financial instruments, optionally filtered by group."""
        return call(self._terminal, "symbols_get", named={"group": group})

    def symbol_info(self, symbol: str) -> JSON:
        """Return data on a financial instrument."""
        return call(self._terminal, "symbol_info", {"symbol": symbol})

    def symbol_info_tick(self, symbol: str) -> JSON:
        """Return the last tick of a financial instrument."""
        return call(self._terminal, "symbol_info_tick", {"symbol": symbol})

    def symbol_select(self, symbol: str, enable: bool | None = None) -> JSON:
        """Select a symbol in MarketWatch, or remove it when enable is False."""
        positional: dict[str, JSON] = {"symbol": symbol}
        if enable is not None:
            positional["enable"] = enable
        return call(self._terminal, "symbol_select", positional)
