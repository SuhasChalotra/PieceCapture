import numpy as np
import gym
from enum import Enum


class GameBoard(gym.Env):

    def __init__(self):
        # GameBoard consists of a matrix of 12x12 elements
        self.Grid = np.zeros([12, 12], dtype=PieceColor)
        return

    def print_grid(self):
        print(self.Grid)
        return


class PieceColor (Enum):
    # Constants that define the state of each GameBoard element
    EMPTY = 0
    RED = 1
    BLUE = 2

