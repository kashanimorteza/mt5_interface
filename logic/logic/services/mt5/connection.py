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

    def __init__(self, terminal: str) -> None:
        """Bind this Function Group to the Terminal of its MT5 instance."""
        self._terminal = terminal

    def initialize(
        self,
        path: str | None = None,
        login: int | None = None,
        password: str | None = None,
        server: str | None = None,
        timeout: int | None = None,
        portable: bool = False,
    ) -> JSON:
        """Establish a connection with the Terminal, starting its Terminal Process.

        `path` defaults to the Terminal's path in config.yaml; any other path is refused.
        """
        configured = resolve(self._terminal).path
        if path is not None and path != configured:
            raise MT5Error(
                INVALID_PARAMS,
                f"parameter 'path' differs from the path of Terminal '{self._terminal}'",
            )
        return call(
            self._terminal,
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

    def login(
        self,
        login: int,
        password: str | None = None,
        server: str | None = None,
        timeout: int | None = None,
    ) -> JSON:
        """Connect to a trading account."""
        return call(
            self._terminal,
            "login",
            {"login": login},
            {"password": password, "server": server, "timeout": timeout},
        )

    def shutdown(self) -> JSON:
        """Close the connection to the Terminal and end its Terminal Process."""
        return call(self._terminal, "shutdown")

    def version(self) -> JSON:
        """Return the Terminal version, build, and release date as a Timestamp."""
        result = call(self._terminal, "version")
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

    def last_error(self) -> JSON:
        """Return the last error code and description."""
        return call(self._terminal, "last_error")

    def account_info(self) -> JSON:
        """Return info on the current trading account."""
        return call(self._terminal, "account_info")

    def terminal_info(self) -> JSON:
        """Return the Terminal status and settings."""
        return call(self._terminal, "terminal_info")
