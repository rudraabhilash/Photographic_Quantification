from abc import ABC, abstractmethod

# Strategy Interface
class FeeStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, trade_value):
        pass


# Concrete Strategies
class EquityFee(FeeStrategy):
    def calculate_fee(self, trade_value):
        return 0.001 * trade_value  # 0.1%


class FuturesFee(FeeStrategy):
    def calculate_fee(self, trade_value):
        return 20  # flat fee


class OptionsFee(FeeStrategy):
    def calculate_fee(self, trade_value):
        return 50  # per lot


# Context
class Trade:
    def __init__(self, trade_value, fee_strategy: FeeStrategy):
        self.trade_value = trade_value
        self.fee_strategy = fee_strategy

    def transaction_cost(self):
        return self.fee_strategy.calculate_fee(self.trade_value)
# Example Usage
if __name__ == "__main__":
    trade1 = Trade(1_000_000, EquityFee())
    trade2 = Trade(1_000_000, FuturesFee())
    print(trade1.transaction_cost())  # 1000.0
    print(trade2.transaction_cost())  # 20
