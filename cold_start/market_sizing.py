class MarketSizing:
    def __init__(self, total_market, target_percentage, capture_rate):
        """
        total_market: total possible users (TAM)
        target_percentage: % of market relevant to product (SAM)
        capture_rate: % you can realistically capture (SOM)
        """
        self.total_market = total_market
        self.target_percentage = target_percentage
        self.capture_rate = capture_rate

    def calculate(self):
        tam = self.total_market
        sam = tam * self.target_percentage
        som = sam * self.capture_rate

        return {
            "TAM": tam,
            "SAM": sam,
            "SOM": som
        }

    def get_max_users(self):
        """
        Returns SOM → used as K in growth model
        """
        return self.total_market * self.target_percentage * self.capture_rate