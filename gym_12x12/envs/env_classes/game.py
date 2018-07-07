from gym_12x12.envs.env_classes.gameboard import GameBoard as gb
from gym_12x12.envs.env_classes.player import Player


class Game:
    GAME_MOVE_INVALID = -1
    GAME_MOVE_VALID = 0
    EMPTY = 0
    RED_PIECE = 2
    BLUE_PIECE = 1

    def __init__(self, player_1, player_2, rows=12, cols=12):
        """
        Initializes a new game.
        :param player_1: The blue player object
        :param player_2: The red player object
        :param rows: on the Y-axis [rows, cols]
        :param cols: on the X-axis [rows, cols]
        """
        # Must ensure that the correct object type is passed as parameters

        if isinstance(player_1, Player):
            self.Player1 = player_1
        else:
            raise ValueError("Player 1: type must be of type Player")

        if isinstance(player_2, Player):
            self.Player2 = player_2
        else:
            raise ValueError("Player 2: type must be of type Player")

        self.__assign_player_piece_color()  # ensure piece colors are different for each player
        #  Create a new game board
        self.Board = gb(size_y=rows, size_x=cols)

        # These fields keep track of players' scores
        self.PlayerOneScore = 0
        self.PlayerTwoScore = 0

        # Keep track of the move number
        self.MoveNumber = 0
        self.empty_spots = []

        #Populate the empty spots list
        for x in range(rows):
            for y in range(cols):
                self.empty_spots.append((x, y))

    def __assign_player_piece_color(self):
        """
        This private method will ensure that the Player1 is BLUE and Player2 is RED
        """
        self.Player1.piece_color = Game.BLUE_PIECE
        self.Player2.piece_color = Game.RED_PIECE

    def place_piece(self, arg_player: Player, yloc, xloc):
        """
        This will place a player's piece in the game_board matrix
        :param arg_player: the player making the move
        :param yloc: Y-axis
        :param xloc: X-axis
        :return: int. Either Game move is VALID or INVALID
        """
        # yloc and xloc need to be within range and be valid integers
        if not isinstance(yloc, int):
            print("y location must be an integer")
            return Game.GAME_MOVE_INVALID

        if not isinstance(xloc, int):
            print("x location must be an integer")
            return Game.GAME_MOVE_INVALID

        if xloc < 0 or xloc > self.Board.COL_COUNT - 1:
            print("x is out of range. x=", xloc)
            return Game.GAME_MOVE_INVALID

        if yloc < 0 or yloc > self.Board.ROW_COUNT - 1:
            print("y is out of range. y=", yloc)
            return Game.GAME_MOVE_INVALID

        if self.Board.Grid[yloc, xloc] == Game.EMPTY:  # Empty slot to play
            self.Board.Grid[yloc, xloc] = arg_player.piece_color
            self.empty_spots.remove(yloc, xloc)

            # self.sweep_board()
            print("Reward check on Move # ", self.MoveNumber, self.reward_check(yloc, xloc))
            self.MoveNumber += 1  # Increment
            return Game.GAME_MOVE_VALID

        else:
            """ The attempting player should be allowed to play another move until the move entered is valid.
            We'll return a value to indicate to the calling code
            that the game move is invalid, and that the player should try again.
            This will only ever happen with human players. The AI can never attempt to play a piece
            in a slot that is occupied, as it will check before doing so. It also can never
            play an invalid move (ex. index out of range)
            """
            print("Invalid move. Try again.")
            return Game.GAME_MOVE_INVALID

    def print_game_board(self):
        # This prints the game board contents
        print(self.Board.Grid)

    def sweep_board(self):
        """
        This scans the game board spot-by-spot and tallies the scores for blue and red.
        :return: void.
        """
        int_blue_score_tally = 0
        int_red_score_tally = 0

        # As a test, let's iterate through entire board
        for r_rows in range(0, len(self.Board.Grid)):
            for c_cols in range(0, self.Board.COL_COUNT):
                if self.Board.Grid[r_rows, c_cols] == Game.EMPTY:
                    continue  # go to next iteration
                if self.Board.Grid[r_rows, c_cols] == Game.BLUE_PIECE:
                    if self.piece_surrounded_alt(r_rows, c_cols):
                        print("Red scores a point",r_rows,c_cols)
                        int_red_score_tally += 1
                elif self.Board.Grid[r_rows, c_cols] == Game.RED_PIECE:
                    if self.piece_surrounded_alt(r_rows, c_cols):
                        print("Blue scores a point",r_rows,c_cols)
                        int_blue_score_tally += 1

        # calc the final score count
        self.PlayerOneScore = int_blue_score_tally
        self.PlayerTwoScore = int_red_score_tally

    def reward_check(self, row, col):
        """
        This function is the alternative to sweep board, which sweeps the entire board and re-tallies the entire score.
        Instead this function should only check the piece currently placed and its surroundings
        :param row:
        :param col:
        :return:
        """
        int_blue_score_tally = 0
        int_red_score_tally = 0

        surrounding_pieces = self.get_surrounding_pieces(row, col)

        # First check if current piece is surrounded
        if self.piece_surrounded_alt(row, col, adjacent_pieces=surrounding_pieces):
            if self.Board.Grid[row, col] == Game.BLUE_PIECE:
                int_red_score_tally += 1
            elif self.Board.Grid[row, col] == Game.RED_PIECE:
                int_blue_score_tally += 1

        # Now we check the adjacent pieces to see if they got surrounded
        for piece in surrounding_pieces:
            if self.Board.Grid[piece[0], piece[1]] == Game.EMPTY:
                continue
            elif self.piece_surrounded_alt(piece[0], piece[1]):
                if self.Board.Grid[piece[0], piece[1]] == Game.BLUE_PIECE:
                    int_red_score_tally += 1
                elif self.Board.Grid[piece[0], piece[1]] == Game.RED_PIECE:
                    int_blue_score_tally += 1

        return [int_blue_score_tally, int_red_score_tally]


    def __is_piece_surrounded(self, at_row, at_col):
        """
        This private function determines if a game piece located at [row, col] is surrounded by an opposing piece
        :param at_row: on the Y axis
        :param at_col: on the X axis
        :return: boolean - if a piece located at [row, col] is surrounded, return True
        """
        opp_color = self.__get_opposing_color(self.Board.Grid[at_row, at_col])

        # Check the corners
        # Top LEFT
        if (at_row, at_col) == self.Board.SPOT_TOP_LEFT:
            if self.Board.Grid[at_row, at_col + 1] == opp_color and self.Board.Grid[at_row + 1, at_col] == opp_color:
                return True

        # TOP RIGHT
        if (at_row, at_col) == self.Board.SPOT_TOP_RIGHT:
            if self.Board.Grid[at_row, at_col - 1] == opp_color and self.Board.Grid[at_row + 1, at_col] == opp_color:
                return True

        # BOTTOM LEFT
        if (at_row, at_col) == self.Board.SPOT_BOTTOM_LEFT:
            if self.Board.Grid[at_row - 1, at_col] == opp_color and self.Board.Grid[at_row, at_col + 1] == opp_color:
                return True
        # BOTTOM RIGHT
        if (at_row, at_col) == self.Board.SPOT_BOTTOM_RIGHT:
            if self.Board.Grid[at_row - 1, at_col] == opp_color and self.Board.Grid[at_row, at_col - 1] == opp_color:
                return True

        # Check the outer edges (excluding corners)
        # TOP EDGE
        if at_row == 0 and at_col >= 1 and at_col <= self.Board.COL_COUNT - 2:
            if self.Board.Grid[at_row, at_col - 1] == opp_color and self.Board.Grid[at_row + 1, at_col] and \
                    self.Board.Grid[at_row, at_col + 1]:
                return True

        # BOTTOM edge
        if at_row == self.Board.ROW_COUNT - 1 and at_col >= 1 and at_col <= self.Board.COL_COUNT - 2:
            if self.Board.Grid[at_row, at_col - 1] == opp_color and self.Board.Grid[at_row - 1, at_col] and \
                    self.Board.Grid[at_row, at_col + 1]:
                return True

        # LEFT EDGE
        if at_col == 0 and at_row >= 1 and at_row <= self.Board.ROW_COUNT - 1:
            if self.Board.Grid[at_row - 1, at_col] == opp_color and self.Board.Grid[at_row + 1, at_col] and \
                    self.Board.Grid[at_row, at_col + 1]:
                return True

        # RIGHT EDGE
        if at_col == self.Board.COL_COUNT - 1 and at_row >= 1 and at_row <= self.Board.ROW_COUNT - 2:
            if self.Board.Grid[at_row - 1, at_col] == opp_color and self.Board.Grid[at_row, at_col - 1] and \
                    self.Board.Grid[at_row + 1, at_col]:
                return True

        # Check for inner space
        if self.Board.Grid[at_row, at_col - 1] == opp_color and self.Board.Grid[at_row - 1, at_col] == opp_color and \
                self.Board.Grid[at_row, at_col + 1] == opp_color and self.Board.Grid[at_row + 1, at_col] == opp_color:
            return True

        #  When all else fails, return false
        return False

    @staticmethod
    def __get_opposing_color(in_color):
        """
        :param in_color: the piece color of which we want to find the opposite color
        ie. if in_color is BLUE, return RED. If in_color is RED, return BLUE
        :return: int - either Game.BLUE_PIECE or Game.RED_PIECE
        """
        if in_color == Game.RED_PIECE:
            return Game.BLUE_PIECE
        elif in_color == Game.BLUE_PIECE:
            return Game.RED_PIECE
        else:
            raise ValueError("Invalid piece color / integer")

    def is_game_complete(self):
        """
        Checks the game board for any empty spots. If none are available, then the game is complete and return true
        else, return false.
        :return: boolean. returns True if there are no empty spots left on the game board
        """
        for y_range in self.Board.Grid:
            for x_range in y_range:
                if self.Board.Grid[y_range, x_range] == Game.EMPTY:  # Encountered an empty tile. immediately return false
                    return False

        return True

    def piece_surrounded_alt(self,row, col, adjacent_pieces = None):

        if not adjacent_pieces:
            surrounding_pieces = self.get_surrounding_pieces(row, col)
        else:
            surrounding_pieces = adjacent_pieces

        opp_color = self.__get_opposing_color(self.Board.Grid[row, col])

        for piece in surrounding_pieces:
            if self.Board.Grid[piece[0],piece[1]] != opp_color:
                return False
        return True

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
        elif row == (self.Board.ROW_COUNT - 1):
            output.pop(1)
            row_checker += 1

        if col == 0: output.pop(3-row_checker)
        elif col == (self.Board.COL_COUNT - 1): output.pop(2-row_checker)

        return output
