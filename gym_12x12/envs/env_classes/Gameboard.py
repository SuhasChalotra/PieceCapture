import numpy as np


class GameBoard:

    def __init__(self, size_x=12, size_y=12):
        # GameBoard consists of a matrix of 12x12 elements
        self.Grid = np.zeros([size_x, size_y], dtype=int)
        self.XSize = size_x
        self.YSize = size_y
