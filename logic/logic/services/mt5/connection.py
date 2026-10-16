"""Connection Function Group of MT5 Service."""

from datetime import UTC, datetime

from logic.services.mt5.terminal import (
    GENERIC_FAIL,
    INVALID_PARAMS,
    JSON,
    MT5Error,
    call,
    resolve,
)


class Connection:
    """Connect to a Terminal, log in, and read version, error, account, and terminal info."""

    @staticmethod
    def initialize(
        terminal: str,
        path: str | None = None,
        login: int | None = None,
        password: str | None = None,
        server: str | None = None,
        timeout: int | None = None,
        portable: bool = False,
    ) -> JSON:
        """Establish a connection with the Terminal, starting its Terminal Process.

        `path` defaults to the Terminal's path in terminal.config; any other path is refused.
        """
        configured = resolve(terminal).path
        if path is not None and path != configured:
            raise MT5Error(
                INVALID_PARAMS,
                f"parameter 'path' differs from the path of Terminal '{terminal}'",
            )
        return call(
            terminal,
            "initialize",
            {"path": configured},
            {
                "login": login,
                "password": password,
                "server": server,
                "timeout": timeout,
                "portable": portable,
            },
        )

    @staticmethod
    def login(
        terminal: str,
        login: int,
        password: str | None = None,
        server: str | None = None,
        timeout: int | None = None,
    ) -> JSON:
        """Connect to a trading account."""
        return call(
            terminal,
            "login",
            {"login": login},
            {"password": password, "server": server, "timeout": timeout},
        )

    @staticmethod
    def shutdown(terminal: str) -> JSON:
        """Close the connection to the Terminal and end its Terminal Process."""
        return call(terminal, "shutdown")

    @staticmethod
    def version(terminal: str) -> JSON:
        """Return the Terminal version, build, and release date as a Timestamp."""
        result = call(terminal, "version")
        if not isinstance(result, list) or len(result) != 3:
            raise MT5Error(GENERIC_FAIL, "version returned an unexpected result")
        version, build, released = result
        try:
            date = datetime.strptime(str(released), "%d %b %Y").replace(tzinfo=UTC)
        except ValueError:
            raise MT5Error(
                GENERIC_FAIL,
                f"version returned an unreadable release date {released!r}",
            ) from None
        return [version, build, int(date.timestamp())]

    @staticmethod
    def last_error(terminal: str) -> JSON:
        """Return the last error code and description."""
        return call(terminal, "last_error")

    @staticmethod
    def account_info(terminal: str) -> JSON:
        """Return info on the current trading account."""
        return call(terminal, "account_info")

    @staticmethod
    def terminal_info(terminal: str) -> JSON:
        """Return the Terminal status and settings."""
        return call(terminal, "terminal_info")
