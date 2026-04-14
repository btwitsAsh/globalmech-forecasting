class RevenueModel:
    def __init__(self, price, conversion_rate):
        self.price = price
        self.conversion_rate = conversion_rate

    def estimate(self, users):
        paying_users = users * self.conversion_rate
        revenue = paying_users * self.price
        return revenue