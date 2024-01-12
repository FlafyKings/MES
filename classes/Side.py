from classes.Point import Point
import numpy as np


class Side:
    def __init__(self, points: list):
        self.points = []
        for x, y in points:
            self.points.append(Point(x, y))

    def __str__(self) -> str:
        return f'Side: {self.points} \n'
    
    def __repr__(self):
        return str(self)