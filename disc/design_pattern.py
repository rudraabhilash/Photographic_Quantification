# Problem:
# A trading system needs to calculate transaction cost, but the fee logic changes:
# Equity trades → % based
# Futures trades → flat fee
# Options trades → per-lot fee
# We want to switch fee logic without changing the main code. No Growing if-else mess, testable independently, 
# Extensibility(Open/Closed principle) - Add new model WITHOUT touching existing code.

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

#****************************************************************************************************
#****************************************************************************************************

# Problem: Facade design pattern
# A trade execution involves many subsystems:
# Risk check
# Margin check
# Order placement
# Settlement
# Client should not deal with this complexity(massive simplification for clients), no tight coupling to internal components, easy to reuse, 

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

#****************************************************************************************************
#****************************************************************************************************
Command design pattern - 

import numpy as np
from abc import ABC, abstractmethod

# -----------------------------
# Receiver (business logic)
# -----------------------------
class CreditRiskEngine:
    def calculate_pd(self, features):
        z = -1 + 0.00001 * features["income"] + 0.7 * features["delinquencies"]
        return 1 / (1 + np.exp(-z))

    def stress_test(self, pd, shock):
        if shock < 0:
            raise ValueError("Shock cannot be negative")  # simulate failure
        return min(1.0, pd * (1 + shock))

    def generate_report(self, pd):
        return {
            "PD": pd,
            "rating": "High Risk" if pd > 0.5 else "Low Risk"
        }


# -----------------------------
# Command Interface
# -----------------------------
class Command(ABC):
    def __init__(self):
        self.result = None
        self.status = "PENDING"  # PENDING, SUCCESS, FAILED

    @abstractmethod
    def execute(self):
        pass


# -----------------------------
# Concrete Commands
# -----------------------------
class ComputePDCommand(Command):
    def __init__(self, engine, features):
        super().__init__()
        self.engine = engine
        self.features = features

    def execute(self):
        self.result = self.engine.calculate_pd(self.features)
        return self.result


class StressTestCommand(Command):
    def __init__(self, engine, pd_command, shock):
        super().__init__()
        self.engine = engine
        self.pd_command = pd_command  # dependency
        self.shock = shock

    def execute(self):
        pd = self.pd_command.result
        if pd is None:
            raise ValueError("PD not computed")

        self.result = self.engine.stress_test(pd, self.shock)
        return self.result


class ReportCommand(Command):
    def __init__(self, engine, stress_command):
        super().__init__()
        self.engine = engine
        self.stress_command = stress_command

    def execute(self):
        pd = self.stress_command.result
        if pd is None:
            raise ValueError("Stress PD missing")

        self.result = self.engine.generate_report(pd)
        return self.result


# -----------------------------
# Pipeline Runner with Retry + Checkpoints
# -----------------------------
class PipelineExecutor:
    def __init__(self):
        self.checkpoints = []  # stores executed commands

    def run(self, commands):
        """
        Runs full pipeline or resumes from partial state.
        Returns index of failed command or None if success.
        """
        for idx, cmd in enumerate(commands):
            if cmd.status == "SUCCESS":
                continue  # skip already completed

            try:
                print(f"Running: {cmd.__class__.__name__}")
                cmd.execute()
                cmd.status = "SUCCESS"
                self.checkpoints.append(cmd)

            except Exception as e:
                cmd.status = "FAILED"
                print(f"❌ Failed at {cmd.__class__.__name__}: {e}")
                return idx  # return failure index

        return None  # success

    def retry_failed(self, commands, failed_index, max_retries=3):
        """
        Retry only failed command, then resume pipeline
        """
        cmd = commands[failed_index]

        for attempt in range(1, max_retries + 1):
            try:
                print(f"🔁 Retry {attempt}: {cmd.__class__.__name__}")
                cmd.execute()
                cmd.status = "SUCCESS"
                print("✅ Retry successful")

                # resume remaining pipeline
                return self.run(commands[failed_index + 1:])

            except Exception as e:
                print(f"Retry failed: {e}")

        print("❌ All retries failed")
        return failed_index


# -----------------------------
# Usage Example
# -----------------------------
if __name__ == "__main__":
    engine = CreditRiskEngine()

    features = {
        "income": 50000,
        "delinquencies": 2
    }

    # Create commands
    pd_cmd = ComputePDCommand(engine, features)
    stress_cmd = StressTestCommand(engine, pd_cmd, shock=-0.2)  # ❌ will fail
    report_cmd = ReportCommand(engine, stress_cmd)

    commands = [pd_cmd, stress_cmd, report_cmd]

    executor = PipelineExecutor()

    # Step 1: Run pipeline
    failed_index = executor.run(commands)

    # Step 2: Fix issue and retry
    if failed_index is not None:
        print("\nFixing issue (shock → 0.2)\n")
        stress_cmd.shock = 0.2  # fix error

        executor.retry_failed(commands, failed_index)

    print("\nFinal Output:", report_cmd.result)


#Benefits - Audit trails, nice retry logic possible & not rerun everything, no tight coupling(queue, airflow plugging easier), parallel execution possible,
# better testing

#****************************************************************************************************
#****************************************************************************************************


# Observer(Publisher subscriber model)
# Benefits - Add new observer very easily(extensibility), 
# drawback - over engineering, without try catch breaks everything

from abc import ABC, abstractmethod
import numpy as np

# -----------------------------
# Observer Interface
# -----------------------------
class Observer(ABC):
    @abstractmethod
    def update(self, data: dict):
        pass


# -----------------------------
# Concrete Observers
# -----------------------------
class RiskLogger(Observer):
    def update(self, data: dict):
        print(f"[LOG] PD computed: {data['pd']:.4f}")


class RiskAlert(Observer):
    def update(self, data: dict):
        if data["pd"] > 0.5:
            print(f"[ALERT] High risk detected! PD={data['pd']:.4f}")


class RiskDashboard(Observer):
    def update(self, data: dict):
        print(f"[DASHBOARD] Updating dashboard with PD={data['pd']:.4f}")


# -----------------------------
# Subject (Publisher)
# -----------------------------
class CreditRiskModel:
    def __init__(self):
        self.observers = []

    def attach(self, observer: Observer):
        self.observers.append(observer)

    def detach(self, observer: Observer):
        self.observers.remove(observer)

    def notify(self, data: dict):
        for obs in self.observers:
            obs.update(data)

    def compute_pd(self, features: dict):
        z = -1 + 0.00001 * features["income"] + 0.7 * features["delinquencies"]
        pd = 1 / (1 + np.exp(-z))

        # Notify all observers
        self.notify({"pd": pd, "features": features})

        return pd


# -----------------------------
# Usage Example
# -----------------------------
if __name__ == "__main__":
    model = CreditRiskModel()

    # Attach observers
    model.attach(RiskLogger())
    model.attach(RiskAlert())
    model.attach(RiskDashboard())

    # Run model
    features = {
        "income": 40000,
        "delinquencies": 3
    }

    pd = model.compute_pd(features)

#****************************************************************************************************
#****************************************************************************************************

# Factory design pattern

from abc import ABC, abstractmethod
import numpy as np

# -----------------------------
# Product Interface
# -----------------------------
class PDModel(ABC):
    @abstractmethod
    def predict(self, features: dict) -> float:
        pass


# -----------------------------
# Concrete Models
# -----------------------------
class LogisticPDModel(PDModel):
    def predict(self, features: dict) -> float:
        z = -1 + 0.00001 * features["income"] + 0.7 * features["delinquencies"]
        return 1 / (1 + np.exp(-z))


class ScorecardPDModel(PDModel):
    def predict(self, features: dict) -> float:
        score = 0
        if features["income"] > 50000:
            score += 20
        if features["delinquencies"] > 2:
            score -= 30

        return max(0.01, min(0.5, 0.3 - score / 200))


class XGBoostPDModel(PDModel):
    def __init__(self, model_path: str):
        self.model_path = model_path
        # pretend loading model here

    def predict(self, features: dict) -> float:
        # dummy logic
        return 0.25


# -----------------------------
# Factory
# -----------------------------
class PDModelFactory:
    _registry = {}

    @classmethod
    def register(cls, name: str, model_cls):
        cls._registry[name] = model_cls

    @classmethod
    def create(cls, name: str, **kwargs) -> PDModel:
        if name not in cls._registry:
            raise ValueError(f"Unknown model: {name}")

        return cls._registry[name](**kwargs)


# -----------------------------
# Register Models
# -----------------------------
PDModelFactory.register("logistic_v1", LogisticPDModel)
PDModelFactory.register("scorecard_v1", ScorecardPDModel)
PDModelFactory.register("xgb_v2", XGBoostPDModel)


# -----------------------------
# Usage Example
# -----------------------------
if __name__ == "__main__":
    config = {
        "model_name": "logistic_v1"
    }

    features = {
        "income": 60000,
        "delinquencies": 1
    }

    # Create model via factory
    model = PDModelFactory.create(config["model_name"])

    pd = model.predict(features)

    print("PD:", pd)

    # Switch model dynamically
    model2 = PDModelFactory.create("scorecard_v1")
    print("PD (scorecard):", model2.predict(features))




#****************************************************************************************************
#****************************************************************************************************
