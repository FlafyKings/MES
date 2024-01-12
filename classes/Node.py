class Node:
    def __init__(self, id: int, x: float, y: float):
        self.id: int = id
        self.x: float = x
        self.y: float = y
        self.BC: bool = False

    def __str__(self) -> str:
        return f'Node: id: {int(self.id)} x: {self.x}, y: {self.y} BC: {self.BC}'
    
    def __repr__(self):
        return str(self)
