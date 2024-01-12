class GlobalData:
    def __init__(self, alfa: int, tot: int, initialTemp: int, density: int, specificHeat: int, nodesNumber: int, elementsNumber: int, simulationTime: int, simulationStepTime: int, conductivity: int):
        self.SimulationTime = simulationTime
        self.SimulationStepTime = simulationStepTime
        self.Conductivity = conductivity
        self.Alfa = alfa
        self.Tot = tot
        self.InitialTemp = initialTemp
        self.Density = density
        self.SpecificHeat = specificHeat
        self.NodesNumber = nodesNumber
        self.ElementsNumber = elementsNumber


    def __init__(self):
        self.SimulationTime = 0
        self.SimulationStepTime = 0
        self.Conductivity = 0
        self.Alfa = 0
        self.Tot = 0
        self.InitialTemp = 0
        self.Density = 0
        self.SpecificHeat = 0
        self.NodesNumber = 0
        self.ElementsNumber = 0

    def __str__(self) -> str:
        return f'SimulationTime: {self.SimulationTime},\n SimulationStepTime: {self.SimulationStepTime},\n Conductivity: {self.Conductivity},\n Alfa: {self.Alfa},\n Tot: {self.Tot},\n InitialTemp: {self.InitialTemp},\n Density: {self.Density},\n SpecificHeat: {self.SpecificHeat},\n NodesNumber: {self.NodesNumber},\n ElementsNumber: {self.ElementsNumber}'



