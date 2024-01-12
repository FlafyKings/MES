from classes.Point import Point
from classes.SimulationData import SimulationData
from classes.Element import Element
from classes.GlobalData import GlobalData
from classes.Grid import Grid
from classes.Node import Node
from classes.UniversalElements import UniversalElement
import numpy as np


numberofKnots = 2
knotsSquared = 4

if __name__ == "__main__":
    np.set_printoptions(threshold=1000, linewidth=250, precision=6, suppress=True)

    simulationData = SimulationData('C:/Users/kamil/Documents/MES/Test1_4_4.txt')
    # simulationData = SimulationData('C:/Users/kamil/Documents/MES/Test2_4_4_MixGrid.txt')
    # simulationData = SimulationData('C:/Users/kamil/Documents/MES/Test3_31_31_kwadrat.txt')
    # simulationData = SimulationData('C:/Users/kamil/Documents/MES/Test4_31_31_trapez.txt') 

    universalElement = UniversalElement(numberofKnots, int(simulationData.globalData.NodesNumber))

    dNdx = np.zeros((knotsSquared, knotsSquared))
    dNdy = np.zeros((knotsSquared, knotsSquared))

    for i, element in enumerate(simulationData.grid.elements):
        element.pcH = np.zeros((universalElement.knotsSquared, 4, 4))

        for j, point in enumerate(universalElement.gaussIntegration.integrationPoints):
            dxdEta = 0
            dydEta = 0 
            dxdKsi = 0
            dydKsi = 0

            for k in range(universalElement.knotsSquared):
                dxdEta += element.nodes[k].x * universalElement.integrationPointsEta[j][k]
                dydEta += element.nodes[k].y * universalElement.integrationPointsEta[j][k]
                dxdKsi += element.nodes[k].x * universalElement.integrationPointsKsi[j][k]
                dydKsi += element.nodes[k].y * universalElement.integrationPointsKsi[j][k]
            
            element.jMatrix = np.array([[dxdEta, dydEta], 
            [dxdKsi, dydKsi]])

            element.det = np.linalg.det(element.jMatrix)

            element.reversedDet = 1 / element.det
            element.reversedJMatrix = element.reversedDet * np.array([[dydKsi, -dydEta], 
                                                                      [-dxdKsi, dxdEta]])
            
            for k in range(knotsSquared):
                dNdx[j][k] = element.reversedJMatrix[0][0] * universalElement.integrationPointsEta[j][k] + element.reversedJMatrix[0][1] * universalElement.integrationPointsKsi[j][k] 
                dNdy[j][k] = element.reversedJMatrix[1][0] * universalElement.integrationPointsEta[j][k] + element.reversedJMatrix[1][1] * universalElement.integrationPointsKsi[j][k]


            element.calculatePcH(dNdx[j], dNdy[j], j, simulationData.globalData.Conductivity)
            element.calculatePC(simulationData.globalData.SpecificHeat, simulationData.globalData.Density, Point(eta=point[0], ksi=point[1]), j)

        element.calculateH(universalElement.gaussIntegration.weights, universalElement.numberOfKnots)
        element.calculateHbc(universalElement.gaussIntegration.weights, universalElement.sides, simulationData.globalData.Alfa)
        element.calculateC(universalElement.gaussIntegration.weights, universalElement.numberOfKnots)
        element.calculateP(universalElement.gaussIntegration.weights, universalElement.sides, simulationData.globalData.Tot, simulationData.globalData.Alfa)


        for k, itemX in enumerate(element.nodes):
            for l, itemY in enumerate(element.nodes):
                universalElement.globalC[int(itemX.id) - 1][int(itemY.id) - 1] += element.C[l][k]
                universalElement.globalH[int(itemX.id) - 1][int(itemY.id) - 1] += element.finalH[l][k]
                
        for k, item in enumerate(element.nodes):
            universalElement.globalP[int(item.id) - 1] += element.P[k]

    # print("-----------------Global C----------------- \n", universalElement.globalC)
    # # print(data)
    # print("-----------------Global H----------------- \n", universalElement.globalH)
    # print("-----------------Global P----------------- \n", universalElement.globalP)
    for o in range(16):
        print(o, " - ", universalElement.globalP[o])

    print(simulationData)


    simulationData.simulation.runSimulation(universalElement.globalH, universalElement.globalC, universalElement.globalP)

