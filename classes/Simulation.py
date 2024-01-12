import os
import numpy as np


class Simulation:
    def __init__(self, createFileFunction, initialTemp, simulationTime, simulationStep, nodesNumber):
        self.T = []
        self.initialTemp = [int(initialTemp) for x in range(int(nodesNumber))]
        self.simulationTime = int(simulationTime)
        self.simulationStep = int(simulationStep)
        self.createFileFunction = createFileFunction

    def __str__(self) -> str:
        return f'Temperature results: \n {self.T} \n'
    
    def __repr__(self):
        return str(self)
    

    def runSimulation(self, H, C, P):
        temperatures = self.initialTemp
        counter = 0
        self.delete_vtk_files()
        for step in range(self.simulationStep, self.simulationTime + self.simulationStep, self.simulationStep):
            temperatures = np.dot(np.linalg.inv(H + (C / self.simulationStep)), (np.dot((C / self.simulationStep), temperatures) + P))
            print("Time = ", step, ",min_T = ", min(temperatures), ",max_T = ", max(temperatures))
            self.createFileFunction(counter, temperatures)
            counter += 1
    
    def delete_vtk_files(self):
        current_dir = os.getcwd()
        file_list = os.listdir(current_dir)
        for file in file_list:
            if file.endswith('.vtk'):
                os.remove(os.path.join(current_dir, file))