import numpy as np


class GameBoard:
    # We need constants that describe the corners of the game board, regardless of its size
    # This is always going to be zero

    def __init__(self, size_y, size_x):
        # GameBoard consists of a matrix of x by y elements (usually 12 by 12)
        """
        If invalid input is detected in creation of the game board, instead of throwing an exception
        we'll ensure that x = 12, and y = 12
        :param size_x: an integer that should be >= 6
        :param size_y: an integer that should be >= 6
        """

        # size should be of type integer
        if not isinstance(size_x, int):
            size_x = 12
            print("Game_board: Parameter was not of type integer. Defaulting to x=12")
        if not isinstance(size_y, int):
            size_y = 12
            print("Game_board: Parameter was not of type integer. Defaulting to y=12")

        # validate input for the size - x and y should have proper integer values
        # ie, it can't be <= 0. We'll force x and y to be at least 6 and <= 12
        if size_x < 6 or size_x > 12:
            size_x = 12  # default to 12 if receiving invalid input
            print("Invalid integer size for x. Changed to x=12")
        if size_y < 6 or size_y > 12:
            size_y = 12  # default to 12 if receiving invalid input
            print("Invalid integer size for y. Changed to y=12")

        self.Grid = np.zeros([size_y, size_x], dtype=int)
        self.ROW_COUNT = size_x
        self.COL_COUNT = size_y

        self.SPOT_TOP_LEFT = (0, 0)
        self.SPOT_TOP_RIGHT = (0, size_x - 1)
        self.SPOT_BOTTOM_LEFT = (size_y - 1, 0)
        self.SPOT_BOTTOM_RIGHT = (size_y - 1, size_x - 1)

