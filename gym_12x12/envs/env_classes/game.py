from gym_12x12.envs.env_classes.player import Player, AIPlayer, HumanPlayer
from gym_12x12.envs.env_classes.gameboard import GameBoard as gb


class Game:
    # This starts a new game / session. It should be initialized w/ a Gameboard and two player
    # objects

    GAME_MOVE_INVALID = -1
    GAME_MOVE_VALID = 0
    EMPTY = 0
    RED_PIECE = 2
    BLUE_PIECE = 1

    def __init__(self, player_1, player_2, arg_size_x=12, arg_size_y=12):
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
        self.Board = gb(size_x=arg_size_x, size_y=arg_size_y)

        # These fields keep track of players' scores
        self.BlueScore = 0
        self.RedScore = 0

    def __assign_player_piece_color(self):
        # This private method will ensure that the players have unique piece colors and should correct
        # the piece color assignment should it be invalid.
        # We need to check if the Player1 and Player2 fields of the game are null or of the incorrect type

            self.Player1.piece_color = Game.BLUE_PIECE
            self.Player2.piece_color = Game.RED_PIECE

    def place_piece(self, arg_player: Player, xloc, yloc):
        # This will place a player's piece in the game_board matrix
        # We need to make sure it can only place a piece in an empty slot

        # x and y need to be within range and be valid integers
        if not isinstance(xloc, int):
            raise ValueError("x location must be an integer")
            return Game.GAME_MOVE_INVALID

        if not isinstance(yloc, int):
            raise ValueError("y location must be an integer")
            return Game.GAME_MOVE_INVALID

        if xloc < 0 or xloc > self.Board.XSize:
            print("x is out of range. x=", xloc)
            return Game.GAME_MOVE_INVALID

        if yloc < 0 or yloc > self.Board.YSize:
            print("y is out of range. y=", yloc)
            return Game.GAME_MOVE_INVALID

        if self.Board.Grid[xloc, yloc] == Game.EMPTY:  # Empty slot to play
            self.Board.Grid[xloc, yloc] = arg_player.piece_color
            return Game.GAME_MOVE_VALID
        else:
            """ Nothing should really happen, and the attempting player should be allowed to play another move.
            We'll return a value to indicate to the calling code
            that the game move is invalid, and that the player should try again.
            This will only ever happen with human players. The AI will never attempt to play a piece
            in a slot that is occupied, as it will check before doing so. It also should never
            play an invalid move (ex. index out of rage)
            """
            print("Invalid move. Try again.")
            return Game.GAME_MOVE_INVALID

    def print_game_board(self):
        # This prints the game board contents
        print(self.Board.Grid)

    def sweep_board(self):
        """
        This scans the game board and keeps track of the scores
        We have to check the four corners, the edges and the inner board
        :return:
        """
        int_blue_score_tally = 0
        int_red_score_tally = 0

        # As a test, let's iterate through entire board
        for r_rows in range(0, len(self.Board.Grid)):
            for c_cols in range(0, self.Board.XSize):
                if self.Board.Grid[r_rows, c_cols] == Game.EMPTY:
                    continue  # go to next iteration
                if self.Board.Grid[r_rows, c_cols] == Game.BLUE_PIECE:
                    if self.__is_piece_surrounded(r_rows, c_cols):
                        print("Red scores a point")
                        int_red_score_tally += 1
                elif self.Board.Grid[r_rows, c_cols] == Game.RED_PIECE:
                    if self.__is_piece_surrounded(r_rows, c_cols):
                        print("Blue scores a point")
                        int_blue_score_tally += 1

        # calc the final score count
        self.BlueScore = int_blue_score_tally
        self.RedScore = int_red_score_tally

    def __is_piece_surrounded(self, at_row, at_col):
        #  This function returns true if a piece at (col, row) is surrounded by an opposing color
        """
        :param at_col: column
        :param at_row: ro
        :return: boolean
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
        # Check for inner space
        if self.Board.Grid[at_row, at_col - 1] == opp_color and self.Board.Grid[at_row - 1, at_col] == opp_color and self.Board.Grid[at_row, at_col + 1] == opp_color and self.Board.Grid[at_row + 1, at_col] == opp_color:
            return True

        #  When all else fails, return false
        return False

    @staticmethod
    def __get_opposing_color(incolor):
        # if incolor is red, return blue and vice versa
        if incolor == Game.RED_PIECE:
            return Game.BLUE_PIECE
        elif incolor == Game.BLUE_PIECE:
            return Game.RED_PIECE
        else:
            raise ValueError("Invalid piece color / integer")


    def test_fill_inner_tiles(self):
        # this is a test function
        for r_rows in range(1, len(self.Board.Grid) - 1):
            for c_cols in range(1, self.Board.XSize - 1):
                self.Board.Grid[c_cols, r_rows] = Game.RED_PIECE

