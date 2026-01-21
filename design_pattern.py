# Problem:
# A trading system needs to calculate transaction cost, but the fee logic changes:
# Equity trades → % based
# Futures trades → flat fee
# Options trades → per-lot fee
# We want to switch fee logic without changing the main code.

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


# Problem: Facade design pattern
# A trade execution involves many subsystems:
# Risk check
# Margin check
# Order placement
# Settlement
# Client should not deal with this complexity.

# Subsystems
class RiskSystem:
    def check_risk(self, amount):
        return amount < 5_000_000


class MarginSystem:
    def check_margin(self, amount):
        return amount * 0.2  # 20% margin required


class OrderSystem:
    def place_order(self, amount):
        return f"Order placed for ₹{amount}"


# Facade
class TradingFacade:
    def __init__(self):
        self.risk = RiskSystem()
        self.margin = MarginSystem()
        self.order = OrderSystem()

    def execute_trade(self, amount):
        if not self.risk.check_risk(amount):
            return "Trade rejected: Risk limit exceeded"

        margin_required = self.margin.check_margin(amount)
        confirmation = self.order.place_order(amount)

        return {
            "status": "SUCCESS",
            "margin_required": margin_required,
            "confirmation": confirmation
        }
trading = TradingFacade()

result = trading.execute_trade(1_000_000)
print(result)
# Output:
# {'status': 'SUCCESS', 'margin_required': 200000.0, 'confirmation': 'Order placed for ₹1000000'}