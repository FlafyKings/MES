import math
from classes.Node import Node
from classes.Point import Point
import numpy as np

class Element:
    def __init__(self, nodesArray: list[Node]):
        self.nodes = nodesArray
        
        self.pcH = []
        self.H = np.zeros((4,4))
        self.Hbc = np.zeros((4,4))
        self.finalH = np.zeros((4, 4))
        
        self.PC = np.zeros((4, 4, 4))
        self.C = np.zeros((4, 4))

        self.P = np.zeros((4))

        self.jMatrix = np.zeros((2, 2))
        self.reversedJMatrix = np.zeros((2, 2))

        self.det = 0
        self.reversedDet = 0

    def __str__(self) -> str:
        # return f'--Element-- \n Nodes: {self.nodes} \n H Matrix: \n {self.H} \n Hbc Matrix: \n {self.Hbc} \n Final H Matrix: \n {self.finalH}  \n P Vector: {self.P} \n C Matrix: \n {self.C}'
        return f'\n --Element-- \n Hbc Matrix: \n {self.Hbc}'
        # return f'--Element-- \n P C: {self.det} \n'
    
    def __repr__(self):
        return str(self)

    def calculateH(self, weights, numberOfKnots):
        for i in range(numberOfKnots):
            for j in range(numberOfKnots):
                self.H += self.pcH[i * numberOfKnots + j] * weights[i % len(weights)] * weights[j % len(weights)]
    
    def calculatePcH(self, dNdx, dNdy, j, conductivity):
        self.pcH[j] = conductivity * (np.transpose(np.outer(dNdx, dNdx)) + np.outer(dNdy, np.transpose(dNdy))) * self.det
    
    def calculateHbc(self, weights, sides, alpha):
        for i in range(len(self.nodes)):
            tempHbc = np.zeros((4,4))
            if self.nodes[i].BC == True and self.nodes[(i + 1) % len(self.nodes)].BC == True:
                for j, point in enumerate(sides[i].points):
                    tempHbc +=  alpha * np.outer(point.N, np.transpose(point.N)) * weights[j % len(weights)] * self.calculateLenDet(i)
            self.Hbc += tempHbc
        self.calculateFinalH()

    def calculateP(self, weights, sides, temperature, alpha):    
        for i in range(len(self.nodes)):
            tempP = np.zeros((4))
            if self.nodes[i].BC == True and self.nodes[(i + 1) % len(self.nodes)].BC == True:
                for j, point in enumerate(sides[i].points):
                    print(point.N)
                    tempP += point.N * temperature * weights[j % len(weights)] 
                self.P +=  alpha * tempP * self.calculateLenDet(i)
    
    def calculatePC(self, heat, density, point: Point, i):
        self.PC[i] = heat * density * np.outer(point.N, np.transpose(point.N)) * self.det
    
    def calculateC(self, weights, numberOfKnots):
        for i in range(numberOfKnots):
            for j in range(numberOfKnots):
                self.C += self.PC[i * numberOfKnots + j] * weights[i % len(weights)] * weights[j % len(weights)]

    def calculateLenDet(self, i):
        return math.sqrt(pow((self.nodes[i].x - self.nodes[(i + 1) % len(self.nodes)].x), 2) + pow((self.nodes[i].y - self.nodes[(i + 1) % len(self.nodes)].y), 2)) / 2
    
    def calculateFinalH(self):
        self.finalH = self.H + self.Hbc