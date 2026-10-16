"""Symbols Function Group of MT5 Service."""

from logic.services.mt5.terminal import JSON, call


class Symbols:
    """Count, list, inspect, and select financial instruments."""

    @staticmethod
    def symbols_total(terminal: str) -> JSON:
        """Return the number of all financial instruments."""
        return call(terminal, "symbols_total")

    @staticmethod
    def symbols_get(terminal: str, group: str | None = None) -> JSON:
        """Return all financial instruments, optionally filtered by group."""
        return call(terminal, "symbols_get", named={"group": group})

    @staticmethod
    def symbol_info(terminal: str, symbol: str) -> JSON:
        """Return data on a financial instrument."""
        return call(terminal, "symbol_info", {"symbol": symbol})

    @staticmethod
    def symbol_info_tick(terminal: str, symbol: str) -> JSON:
        """Return the last tick of a financial instrument."""
        return call(terminal, "symbol_info_tick", {"symbol": symbol})

    @staticmethod
    def symbol_select(terminal: str, symbol: str, enable: bool | None = None) -> JSON:
        """Select a symbol in MarketWatch, or remove it when enable is False."""
        positional: dict[str, JSON] = {"symbol": symbol}
        if enable is not None:
            positional["enable"] = enable
        return call(terminal, "symbol_select", positional)
