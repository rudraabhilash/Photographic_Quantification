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


        
