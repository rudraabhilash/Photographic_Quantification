# print("Hello!")

# -Name(), size, price


# sum (pricei * sizei)/sum(sizei )


# def update(name, size, price)
# def getavgprice(name): -> ave price of that name

class StockVwap:
    """ 
    Volume weighted average price calculator 
    for different stock names using streaming updates.
    """
    __slots__ = ('sumPriceSize', 'sumSize')

    def __init__(self) -> None:
        self.sumPriceSize: Dict[str, float] = {}
        self.sumSize: Dict[str, int] = {}

    def update(self, symbol: str, price: float, size: int) -> None:
        if size <= 0:
            raise ValueError("Trade size must be positive")

        symbol = symbol.upper()
        if symbol not in self.sumPriceSize:
            self.sumPriceSize[symbol] = 0.0
            self.sumSize[symbol]      = 0

        self.sumPriceSize[symbol] += price * size
        self.sumSize[symbol] += size

    def getVwap(self, symbol: str) -> float:
        symbol = symbol.uppper()
        if symbol not in self.sumPriceSize:
            raise KeyError(f"unknown symbol: {symbol}")
        return self.sumPriceSize[symbol]/self.sumSize[symbol]


import threading
class ThreadSafeStockVwap:
    """ 
    Multithreading safe version 
    Volume weighted average price calculator 
    for different stock names using streaming updates.
    """
    __slots__ = ('_sumPriceSize', '_sumSize', '_lock')

    def __init__(self) -> None:
        self._sumPriceSize: Dict[str, float] = {}
        self._sumSize: Dict[str, int] = {}
        self._lock = threading.Lock()

    def update(self, symbol: str, price: float, size: int) -> None:
        if size <= 0:
            raise ValueError("Trade size must be positive")

        symbol = symbol.upper()
        with self._lock:
            if symbol not in self._sumPriceSize:
                self._sumPriceSize[symbol] = 0.0
                self._sumSize[symbol]      = 0

            self._sumPriceSize[symbol] += price * size
            self._sumSize[symbol] += size

    def getVwap(self, symbol: str) -> float:
        symbol = symbol.upper()
        with self._lock:
            if symbol not in self._sumPriceSize:
                raise KeyError(f"unknown symbol: {symbol}")
            return self._sumPriceSize[symbol] / self._sumSize[symbol]
#since updates are tiny(two dictionary ops) therefore lock contention should be minimal. 
# HFT systems later shard by symbol or CPU core.

