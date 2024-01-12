from classes.Element import Element
from classes.GlobalData import GlobalData
from classes.Grid import Grid
from classes.Node import Node
from classes.Simulation import Simulation


nodesTemp: list[Node] = []
class SimulationData:

    def __init__(self, fileName: str):
        self.globalData = GlobalData()
        self.grid = Grid()
        self.readFromFile(fileName)
        self.simulation = Simulation(self.createVtkFile, self.globalData.InitialTemp, self.globalData.SimulationTime, self.globalData.SimulationStepTime, self.globalData.NodesNumber)

    def __str__(self) -> str:
        return f'--GlobalData--: \n {self.globalData},\n \n {self.grid}'

    def readFromFile(self, fileName: str):
        currentSection = 'GlobalData'
        
        with open(fileName, 'r') as file:
            for i, line in enumerate(file):
                line = line.strip()         
                if line.startswith('*Node'):
                    currentSection = 'Node'
                elif line.startswith('*Element'):
                    currentSection = 'Element'
                elif line.startswith('*BC'):
                    currentSection = 'BC'
                self.readSection(currentSection, line)
                          
    def readSection(self, section, line):
        parts = line.split(',')
        if section == 'GlobalData':
            key, value = line.split()
            if hasattr(self.globalData, key):
                setattr(self.globalData, key, float(value))
        if section == 'Node':
            if len(parts) == 3:
                nodeId, x, y = map(float, parts)
                nodesTemp.append(Node(nodeId, x, y))
        elif section == 'Element':
            if len(parts) >= 5:
                elementData = [int(part) for part in parts]
                elementData = elementData[1:]
                selectedNodes = [findNodeById(id) for id in elementData]
                #DELETE LATER
                # tempNodes = [Node(elementData[0], 0,0), Node(elementData[1], 0.025,0), Node(elementData[2], 0.025,0.025), Node(elementData[3], 0,0.025)]
                # self.grid.elements.append(Element(tempNodes))
                self.grid.elements.append(Element(selectedNodes))
        elif section == 'BC':
            if len(parts) > 2:
                bcData = [int(part) for part in parts]
                for node in nodesTemp:
                    if node.id in bcData:
                        node.BC = True

    def createVtkFile(self, step, vector):
        # Construct the filename using the given step
        filename = f"Foo{step}.vtk"

        with open(filename, 'w') as file:
            # Writing header information to the file
            file.writelines([
                "# vtk DataFile Version 2.0\n",
                "Unstructured Grid Example\n",
                "ASCII\n",
                "DATASET UNSTRUCTURED_GRID\n\n"
            ])

            # Writing the points data
            file.write(f"POINTS {int(self.globalData.NodesNumber)} float\n")
            for node in nodesTemp:
                file.write(f"{node.x} {node.y} 0\n")
            file.write('\n')

            # Writing the cells data
            elements_count = int(self.globalData.ElementsNumber)
            file.write(f"CELLS {elements_count} {elements_count * 5}\n")
            for element in self.grid.elements:
                file.write("4 " + " ".join([str(int(node.id) - 1) for node in element.nodes]) + "\n")
            file.write('\n')

            # Writing the cell types
            file.write(f"CELL_TYPES {elements_count}\n")
            file.write("9\n" * elements_count)
            file.write('\n')

            # Writing the point data
            file.write(f"POINT_DATA {int(self.globalData.NodesNumber)}\n")
            file.writelines([
                "SCALARS Temp float 1\n",
                "LOOKUP_TABLE default\n"
            ])
            file.writelines([f"{temp}\n" for temp in vector])

def findNodeById(nodeId):
    for obj in nodesTemp:
        if obj.id == nodeId:
            return obj
    return None