"""Run the create_tables Setup Operation on the default Instance and report its SetupResult."""

import sys

from database.interface import database_error, database_setup


def main() -> int:
    try:
        result = database_setup().create_tables()
    except database_error.DatabaseError as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        return 1
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
