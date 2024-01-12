from classes.Element import Element

class Grid:
    def __init__(self):
        self.elements: list[Element] = []

    def __str__(self) -> str:
        return f'--Grid-- \n {str(self.elements)}'
    
    def __repr__(self):
        return str(self)