import numpy as np
import itertools

class GaussIntegration:
    def __init__(self, nodesNumber):
        self.weights, self.integrationCords = self.calculate(nodesNumber)
        self.integrationPoints = list(itertools.product(self.integrationCords, repeat=len(self.integrationCords)))


    def calculate(self, nodesNumber):
        integrationPoints, weights = np.polynomial.legendre.leggauss(nodesNumber)

        return weights, integrationPoints