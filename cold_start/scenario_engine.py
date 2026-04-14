import numpy as np
from cold_start.growth_model import GrowthModel
from cold_start.revenue_model import RevenueModel


class ScenarioEngine:
    def __init__(self, K):
        self.K = K

    def run(self, name, growth_rate, price, conversion, t0=12):
        growth = GrowthModel(self.K, growth_rate, t0)
        revenue_model = RevenueModel(price, conversion)

        months = np.arange(0, 36)
        users = growth.predict(months)
        revenue = revenue_model.estimate(users)

        return {
            "name": name,
            "months": months,
            "users": users,
            "revenue": revenue
        }

    def run_all(self):
        scenarios = []

        scenarios.append(self.run(
            name="Best Case",
            growth_rate=0.5,
            price=800,
            conversion=0.1
        ))

        scenarios.append(self.run(
            name="Expected Case",
            growth_rate=0.3,
            price=500,
            conversion=0.05
        ))

        scenarios.append(self.run(
            name="Worst Case",
            growth_rate=0.15,
            price=300,
            conversion=0.02
        ))

        return scenarios