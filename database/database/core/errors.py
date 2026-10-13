"""The base Database error and one error for every declared failure kind."""


class DatabaseError(Exception):
    """The base of every Database error; it never carries a connection value or credential."""


class ConfigurationError(DatabaseError):
    """Invalid configuration or Instance."""


class InactiveInstanceError(DatabaseError):
    """Inactive Instance selected."""


class InvalidInputError(DatabaseError):
    """Invalid input or Field."""


class DeclarationMismatchError(DatabaseError):
    """Declaration incompatibility."""


class ConnectionFailureError(DatabaseError):
    """Connection failure."""


class ExecutionError(DatabaseError):
    """Execution failure."""


class SetupError(DatabaseError):
    """Incomplete Setup execution."""
