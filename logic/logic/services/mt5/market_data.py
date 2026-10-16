"""MarketData Function Group of MT5 Service."""

from logic.services.mt5.terminal import JSON, call, check_timestamp


class MarketData:
    """Retrieve bars and ticks; every date and time is a Timestamp."""

    @staticmethod
    def copy_rates_from(
        terminal: str, symbol: str, timeframe: int, date_from: int, count: int
    ) -> JSON:
        """Return bars starting from a date."""
        check_timestamp("date_from", date_from)
        return call(
            terminal,
            "copy_rates_from",
            {
                "symbol": symbol,
                "timeframe": timeframe,
                "date_from": date_from,
                "count": count,
            },
        )

    @staticmethod
    def copy_rates_from_pos(
        terminal: str, symbol: str, timeframe: int, start_pos: int, count: int
    ) -> JSON:
        """Return bars starting from a bar index."""
        return call(
            terminal,
            "copy_rates_from_pos",
            {
                "symbol": symbol,
                "timeframe": timeframe,
                "start_pos": start_pos,
                "count": count,
            },
        )

    @staticmethod
    def copy_rates_range(
        terminal: str, symbol: str, timeframe: int, date_from: int, date_to: int
    ) -> JSON:
        """Return bars within a date range."""
        check_timestamp("date_from", date_from)
        check_timestamp("date_to", date_to)
        return call(
            terminal,
            "copy_rates_range",
            {
                "symbol": symbol,
                "timeframe": timeframe,
                "date_from": date_from,
                "date_to": date_to,
            },
        )

    @staticmethod
    def copy_ticks_from(
        terminal: str, symbol: str, date_from: int, count: int, flags: int
    ) -> JSON:
        """Return ticks starting from a date."""
        check_timestamp("date_from", date_from)
        return call(
            terminal,
            "copy_ticks_from",
            {"symbol": symbol, "date_from": date_from, "count": count, "flags": flags},
        )

    @staticmethod
    def copy_ticks_range(
        terminal: str, symbol: str, date_from: int, date_to: int, flags: int
    ) -> JSON:
        """Return ticks within a date range."""
        check_timestamp("date_from", date_from)
        check_timestamp("date_to", date_to)
        return call(
            terminal,
            "copy_ticks_range",
            {
                "symbol": symbol,
                "date_from": date_from,
                "date_to": date_to,
                "flags": flags,
            },
        )
