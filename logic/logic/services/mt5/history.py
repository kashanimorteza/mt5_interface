"""History Function Group of MT5 Service."""

from logic.services.mt5.terminal import JSON, call, check_timestamp


def _interval(date_from: int | None, date_to: int | None) -> dict[str, JSON]:
    check_timestamp("date_from", date_from)
    check_timestamp("date_to", date_to)
    if date_from is None and date_to is None:
        return {}
    return {"date_from": date_from, "date_to": date_to}


class History:
    """Count and read historical orders and deals; every date and time is a Timestamp."""

    def __init__(self, terminal: str) -> None:
        """Bind this Function Group to the Terminal of its MT5 instance."""
        self._terminal = terminal

    def history_orders_total(self, date_from: int, date_to: int) -> JSON:
        """Return the number of history orders within an interval."""
        return call(
            self._terminal, "history_orders_total", _interval(date_from, date_to)
        )

    def history_orders_get(
        self,
        date_from: int | None = None,
        date_to: int | None = None,
        group: str | None = None,
        ticket: int | None = None,
        position: int | None = None,
    ) -> JSON:
        """Return history orders within an interval, or by order or position ticket."""
        return call(
            self._terminal,
            "history_orders_get",
            _interval(date_from, date_to),
            {"group": group, "ticket": ticket, "position": position},
        )

    def history_deals_total(self, date_from: int, date_to: int) -> JSON:
        """Return the number of history deals within an interval."""
        return call(
            self._terminal, "history_deals_total", _interval(date_from, date_to)
        )

    def history_deals_get(
        self,
        date_from: int | None = None,
        date_to: int | None = None,
        group: str | None = None,
        ticket: int | None = None,
        position: int | None = None,
    ) -> JSON:
        """Return history deals within an interval, or by order or position ticket."""
        return call(
            self._terminal,
            "history_deals_get",
            _interval(date_from, date_to),
            {"group": group, "ticket": ticket, "position": position},
        )
