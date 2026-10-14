"""The Connection Function Group: one method for every Function MT5 Service lists under Connection."""

from typing import Any

from logic.services.mt5 import terminal as terminal_processes


class Connection:
    """One method for every Function of the Connection Function Group, each run in the Terminal Process of its Terminal."""

    @staticmethod
    def initialize(
        terminal: str,
        path: str | None = None,
        *,
        login: int | None = None,
        password: str | None = None,
        server: str | None = None,
        timeout: int | None = None,
        portable: bool = False,
    ) -> Any:
        """Establish a connection with the MetaTrader 5 terminal."""
        return terminal_processes.open(
            terminal,
            terminal_processes.given(path=path),
            terminal_processes.named(
                login=login,
                password=password,
                server=server,
                timeout=timeout,
                portable=portable,
            ),
            (False,),
        )

    @staticmethod
    def login(
        terminal: str,
        login: int,
        *,
        password: str | None = None,
        server: str | None = None,
        timeout: int | None = None,
    ) -> Any:
        """Connect to a trading account using specified parameters."""
        return terminal_processes.call(
            terminal,
            "login",
            terminal_processes.given(login=login),
            terminal_processes.named(password=password, server=server, timeout=timeout),
            (False,),
        )

    @staticmethod
    def shutdown(terminal: str) -> Any:
        """Close the previously established connection to the MetaTrader 5 terminal."""
        return terminal_processes.call(terminal, "shutdown", (), {}, ())

    @staticmethod
    def version(terminal: str) -> Any:
        """Return the MetaTrader 5 terminal version."""
        return terminal_processes.call(terminal, "version", (), {}, (None,))

    @staticmethod
    def last_error(terminal: str) -> Any:
        """Return data on the last error."""
        return terminal_processes.call(terminal, "last_error", (), {}, ())

    @staticmethod
    def account_info(terminal: str) -> Any:
        """Get info on the current trading account."""
        return terminal_processes.call(terminal, "account_info", (), {}, (None,))

    @staticmethod
    def terminal_info(terminal: str) -> Any:
        """Get the connected MetaTrader 5 client terminal status and settings."""
        return terminal_processes.call(terminal, "terminal_info", (), {}, (None,))
