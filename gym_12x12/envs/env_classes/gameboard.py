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

        # Keeps track of empty spots
        self.empty_spots = []
        # Populate the empty spots list
        for x in range(size_y):
            for y in range(size_x):
                self.empty_spots.append((x, y))

    def get_surrounding_pieces(self, row, col, diagonals=False):
        """
        This function will return  a list of the 2-4 surrounding pieces
        :param row:
        :param col:
        :param diagonals: if set to true, the surrounding pieces will be checked at the diagonal
        ie. up-left, up-right, bottom-left, bottom-right
        :return:
        """
        output = []
        if not diagonals:
            # These are the top, bottom, right and left pieces
            output = [[row-1,col],[row+1,col],[row,col+1],[row,col-1]]
            row_checker = 0

            if row == 0:
                output.pop(0)
                row_checker += 1
            elif row == (self.ROW_COUNT - 1):
                output.pop(1)
                row_checker += 1

            if col == 0:
                output.pop(3 - row_checker)
            elif col == (self.COL_COUNT - 1):
                output.pop(2 - row_checker)
        else:
            # These are the diagonals from the center piece at question
            output = [[row - 1, col - 1], [row - 1, col + 1], [row + 1, col - 1], [row + 1, col + 1]]
            output = self._remove_invalid_tuples(output)

        return output

    def clear(self):
        # Clear the game grid
        self.Grid = np.zeros([self.ROW_COUNT, self.COL_COUNT], dtype=int)

    def _remove_invalid_tuples(self, surrounding_p):
        """
        This function removes any tuples [row, col] where row and/or col are out of bounds
        :param surrounding_p: a list of surrounding pieces
        :return: a list of surrounding pieces that only has valid [row, col]
        """
        return_list = []

        if isinstance(surrounding_p, list):

            for co_ord in range(len(surrounding_p)):
                row, col = surrounding_p[co_ord]

                if row >= 0 and row < self.ROW_COUNT:
                    if col >= 0 and col < self.COL_COUNT:
                        return_list.append(surrounding_p[co_ord])

        else:
            raise ValueError("Not a list")

        return return_list

    def get_count_of(self, piece_color, in_list):
        """
        :param piece_color: 0, 1 or 2 - the items we are looking for
        :param in_list: a list
        :return: returns an integer containing the amount of times piece_color appears in the array
        """

        count = 0
        if isinstance(in_list, list) or isinstance(in_list, tuple):
            for i in range(0, len(in_list)):
                r, c = in_list[i]
                if self.Grid[r, c] == piece_color:
                    count += 1

        else:
            raise ValueError("in_list must be a list or tuple")

        return count
