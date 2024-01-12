from Gauss import GaussIntegration
from classes.IntegrationPoint import IntegrationPoint
from classes.Point import Point
from classes.Side import Side
import numpy as np
import math

class UniversalElement:
    def __init__(self, numberOfKnots: int, nodesNumber: int):
        self.numberOfKnots = numberOfKnots
        self.knotsSquared = numberOfKnots * numberOfKnots

        self.gaussIntegration = GaussIntegration(numberOfKnots) 

        self.integrationPoints: list[Point] = self.populateIntegrationPoints()

        self.integrationPointsEta, self.integrationPointsKsi = self.calculateEtaKsi()

        self.sides: list[Side] = self.populateSidePoints()

        #Agregation
        self.globalH = np.zeros((nodesNumber, nodesNumber))
        self.globalP = np.zeros((nodesNumber))
        self.globalC = np.zeros((nodesNumber, nodesNumber))
   
    def calculateEtaKsi(self):
        tempEta = np.zeros((self.knotsSquared, 4))
        tempKsi = np.zeros((self.knotsSquared, 4))
        for i in range(self.knotsSquared):
            for j in range(4):
                tempEta[i][j] = self.calculateEtaValues(self.gaussIntegration.integrationCords[i // self.numberOfKnots], j)
                tempKsi[i][j] = self.calculateKsiValues(self.gaussIntegration.integrationCords[i % self.numberOfKnots], j)
        return tempEta, tempKsi

    def calculateEtaValues(self, value, index):
        if index == 0:
            return - 0.25 * (1 - value)
        elif index == 1:
            return 0.25 * (1 - value)
        elif index == 2:
            return 0.25 * (1 + value)
        elif index == 3:
            return - 0.25 * (1 + value)

    def calculateKsiValues(self, value, index):
        if index == 0:
            return - 0.25 * (1 - value)
        elif index == 1:
            return - 0.25 * (1 + value)
        elif index == 2:
            return 0.25 * (1 + value)
        elif index == 3:
            return 0.25 * (1 - value)
    
    def populateSidePoints(self):
        firstSide = set() # y = -1
        secondSide = set() # x = 1
        thirdSide = set() # y = 1
        fourthSide = set() # x = -1
        for x, y in self.gaussIntegration.integrationPoints:
            firstSide.add((x, -1))
            secondSide.add((1, y))
            thirdSide.add((x, 1))
            fourthSide.add((-1, y))
        
        return [Side(firstSide), Side(secondSide), Side(thirdSide), Side(fourthSide)]

    def populateIntegrationPoints(self):
        integrationPointsTemp = []
        for point in self.gaussIntegration.integrationPoints:
            integrationPointsTemp.append(Point(point[0], point[1]))
        return integrationPointsTemp