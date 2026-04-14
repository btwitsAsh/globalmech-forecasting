class GeoModel:
    def __init__(self, region):
        self.region = region

        self.region_factors = {
            "India": {
                "adoption": 0.8,
                "conversion": 0.7,
                "price": 0.6
            },
            "USA": {
                "adoption": 1.2,
                "conversion": 1.1,
                "price": 1.5
            },
            "Europe": {
                "adoption": 1.0,
                "conversion": 0.9,
                "price": 1.2
            }
        }

    def adjust(self, growth_rate, conversion, price):
        factors = self.region_factors[self.region]

        return {
            "growth_rate": growth_rate * factors["adoption "],
            "conversion": conversion * factors["conversion"],
            "price": price * factors["price"]
        }