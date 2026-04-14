import numpy as np

class GeoModelV2:
    def __init__(self, region):
        self.region = region

        # 📊 Realistic macro indicators (normalized-ish)
        self.region_data = {
            "India": {
                "internet_penetration": 0.6,
                "gdp_per_capita": 2500,
                "digital_payments": 0.7
            },
            "USA": {
                "internet_penetration": 0.9,
                "gdp_per_capita": 70000,
                "digital_payments": 0.9
            },
            "Europe": {
                "internet_penetration": 0.85,
                "gdp_per_capita": 45000,
                "digital_payments": 0.85
            }
        }

    def normalize_gdp(self, gdp):
        # normalize GDP to scale ~0.5 to 1.5
        return np.clip(gdp / 50000, 0.5, 1.5)

    def compute_factors(self):
        data = self.region_data[self.region]

        adoption = data["internet_penetration"]
        conversion = data["digital_payments"]
        price = self.normalize_gdp(data["gdp_per_capita"])

        return {
            "adoption": adoption,
            "conversion": conversion,
            "price": price
        }

    def adjust(self, growth_rate, conversion, price):
        factors = self.compute_factors()

        return {
            "growth_rate": growth_rate * factors["adoption"],
            "conversion": conversion * factors["conversion"],
            "price": price * factors["price"]
        }