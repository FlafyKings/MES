import numpy as np


class Point:
    def __init__(self, ksi: float, eta: float):
        self.ksi = ksi
        self.eta = eta
        self.N = self.calculateShape()
        
    def calculateShape(self):
        N1 = 0.25 * (1 - self.ksi) * (1 - self.eta)
        N2 = 0.25 * (1 + self.ksi) * (1 - self.eta)
        N3 = 0.25 * (1 + self.ksi) * (1 + self.eta)
        N4 = 0.25 * (1 - self.ksi) * (1 + self.eta)
        
        return np.array([N1, N2, N3, N4])

    def __str__(self) -> str:
        return f'ksi: {self.ksi}, eta: {self.eta}'
    
    def __repr__(self):
        return str(self)