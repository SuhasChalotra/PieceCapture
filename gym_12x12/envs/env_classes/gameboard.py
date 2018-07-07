import numpy as np


class GameBoard:
    """
    The Game board is a property of the Game class. It consists of a grid of [rows, cols], typically
    6x6 or 12x12. This is a matrix upon which the players place their pieces.
    """
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

        self.Grid = np.zeros([size_y, size_x], dtype=int)  # This is the main matrix

        self.ROW_COUNT = size_x
        self.COL_COUNT = size_y

        self.SPOT_TOP_LEFT = (0, 0)
        self.SPOT_TOP_RIGHT = (0, size_x - 1)
        self.SPOT_BOTTOM_LEFT = (size_y - 1, 0)
        self.SPOT_BOTTOM_RIGHT = (size_y - 1, size_x - 1)

    def get_surrounding_pieces(self, row, col):
        """
        This function will return  a list of the 2-4 surrounding pieces
        :param row:
        :param col:
        :return:
        """
        output = [[row-1,col],[row+1,col],[row,col+1],[row,col-1]] # These are the top, bottom, right and left pieces
        row_checker = 0

        if row == 0:
            output.pop(0)
            row_checker += 1
        elif row == (self.ROW_COUNT - 1):
            output.pop(1)
            row_checker += 1

        if col == 0: output.pop(3-row_checker)
        elif col == (self.COL_COUNT - 1): output.pop(2-row_checker)

        return output

    def clear(self):
        # Clear the game grid
        self.Grid = np.zeros([self.ROW_COUNT, self.COL_COUNT], dtype=int)
