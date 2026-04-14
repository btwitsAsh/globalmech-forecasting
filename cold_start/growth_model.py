import numpy as np

class GrowthModel:
    def __init__(self, K, r, t0):
        self.K = K
        self.r = r
        self.t0 = t0

    def predict(self, t):
        return self.K / (1 + np.exp(-self.r * (t - self.t0)))