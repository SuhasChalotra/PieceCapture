import numpy as np
import gym

class GameBoard(gym.Env):

    def __init__(self):
        # GameBoard consists of a matrix of 12x12 elements
        self.Grid = np.zeros([12, 12], dtype=int)
        return

    def print_grid(self):
        print(self.Grid)
        return

