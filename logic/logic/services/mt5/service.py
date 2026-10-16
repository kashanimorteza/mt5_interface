"""MT5 class of MT5 Service: every Function Group bound to one Terminal."""

from logic.services.mt5.connection import Connection
from logic.services.mt5.history import History
from logic.services.mt5.market_book import MarketBook
from logic.services.mt5.market_data import MarketData
from logic.services.mt5.orders import Orders
from logic.services.mt5.positions import Positions
from logic.services.mt5.symbols import Symbols
from logic.services.mt5.terminal import find


class MT5:
    """One MT5 instance: the Function Groups of the Terminal named at creation.

    Creating it opens no connection; `Connection.initialize` starts the Terminal's process.
    Any number of instances may exist at once, and instances of one Terminal share its process.
    """

    def __init__(self, terminal: str) -> None:
        """Bind a new MT5 instance to a Terminal in config.yaml, refusing an unknown name."""
        name = find(terminal).name
        self.Connection = Connection(name)
        self.Symbols = Symbols(name)
        self.MarketBook = MarketBook(name)
        self.MarketData = MarketData(name)
        self.Orders = Orders(name)
        self.Positions = Positions(name)
        self.History = History(name)
