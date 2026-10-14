"""The History Function Group: one method for every Function MT5 Service lists under History."""

from typing import Any

from logic.services.mt5 import terminal as terminal_processes


class History:
    """One method for every Function of the History Function Group, each run in the Terminal Process of its Terminal."""

    @staticmethod
    def history_orders_total(terminal: str, date_from: int, date_to: int) -> Any:
        """Get the number of orders in trading history within the specified interval."""
        return terminal_processes.call(
            terminal,
            "history_orders_total",
            terminal_processes.given(date_from=date_from, date_to=date_to),
            {},
            (None,),
        )

    @staticmethod
    def history_orders_get(
        terminal: str,
        date_from: int | None = None,
        date_to: int | None = None,
        *,
        group: str | None = None,
        ticket: int | None = None,
        position: int | None = None,
    ) -> Any:
        """Get orders from trading history with the ability to filter by ticket or position."""
        return terminal_processes.call(
            terminal,
            "history_orders_get",
            terminal_processes.given(date_from=date_from, date_to=date_to),
            terminal_processes.named(group=group, ticket=ticket, position=position),
            (None,),
        )

    @staticmethod
    def history_deals_total(terminal: str, date_from: int, date_to: int) -> Any:
        """Get the number of deals in trading history within the specified interval."""
        return terminal_processes.call(
            terminal,
            "history_deals_total",
            terminal_processes.given(date_from=date_from, date_to=date_to),
            {},
            (None,),
        )

    @staticmethod
    def history_deals_get(
        terminal: str,
        date_from: int | None = None,
        date_to: int | None = None,
        *,
        group: str | None = None,
        ticket: int | None = None,
        position: int | None = None,
    ) -> Any:
        """Get deals from trading history within the specified interval with the ability to filter by ticket or position."""
        return terminal_processes.call(
            terminal,
            "history_deals_get",
            terminal_processes.given(date_from=date_from, date_to=date_to),
            terminal_processes.named(group=group, ticket=ticket, position=position),
            (None,),
        )
