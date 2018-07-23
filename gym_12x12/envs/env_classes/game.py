from gym_12x12.envs.env_classes.gameboard import GameBoard as gb
from gym_12x12.envs.env_classes.player import Player, AgentPlayer, BotPlayer


class Game:
    GAME_MOVE_INVALID = -1
    GAME_MOVE_VALID = 0
    EMPTY = 0
    RED_PIECE = 2
    BLUE_PIECE = 1
    POINT_REWARD = 10
    INVALID_MOVE_PENALIZATION = -1

    def __init__(self, player_1, player_2, rows=12, cols=12):
        """
        Initializes a new game.
        :param player_1: The blue player object
        :param player_2: The red player object
        :param rows: on the Y-axis [rows, cols]
        :param cols: on the X-axis [rows, cols]
        """
        # Must ensure that the correct object type is passed as parameters
        print(type(player_1))
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

        # keep track of game running status
        self.game_is_on = False

    def start(self):
        self.game_is_on = True

    def stop(self):
        self.game_is_on = False

    def reset(self):
        """
        Should reset the game
        :return:
        """
        self.PlayerOneScore = 0
        self.PlayerTwoScore = 0
        self.Board.clear()  # this should reset empty spots and clear the game board

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
        :param yloc: Rows (vertical)
        :param xloc: Columns (horizontal)
        :return: int, int_p1_pointScored, int_p2_pointScored
        """
        if not self.game_is_on:
            raise ValueError("Game has not started")

        # if self.is_game_complete():
        #     # Game is completed
        #     self.game_is_on = False
        #     return

        # yloc and xloc need to be within range and be valid integers
        if arg_player.piece_color == Game.BLUE_PIECE:
            blue_reward = Game.INVALID_MOVE_PENALIZATION
            red_reward = 0
        elif arg_player.piece_color == Game.RED_PIECE:
            red_reward = Game.INVALID_MOVE_PENALIZATION
            blue_reward = 0

        if not isinstance(yloc, int):
            print("y location must be an integer")
            return Game.GAME_MOVE_INVALID, blue_reward, red_reward

        if not isinstance(xloc, int):
            print("x location must be an integer")
            return Game.GAME_MOVE_INVALID, blue_reward, red_reward

        if xloc < 0 or xloc > self.Board.COL_COUNT - 1:
            print("x is out of range.", yloc, ",", xloc)
            return Game.GAME_MOVE_INVALID, blue_reward, red_reward

        if yloc < 0 or yloc > self.Board.ROW_COUNT - 1:
            print("y is out of range.", yloc, ",", xloc)
            return Game.GAME_MOVE_INVALID, blue_reward, red_reward

        if self.Board.Grid[yloc, xloc] == Game.EMPTY:  # Empty slot to play
            self.Board.Grid[yloc, xloc] = arg_player.piece_color

            # self.sweep_board()
            print("Reward check on Move # ", self.MoveNumber, self.reward_check(yloc, xloc))
            reward_results = self.reward_check(yloc, xloc)
            self.MoveNumber += 1  # Increment the score
            self.Board.empty_spots.remove((yloc, xloc))
            print("removed ", yloc, ",", xloc, "empty moves left=", len(self.Board.empty_spots))
            return Game.GAME_MOVE_VALID,  reward_results[0], reward_results[1]

        else:
            print(yloc, xloc, " is an Invalid move. Try again.")
            return Game.GAME_MOVE_INVALID, blue_reward, red_reward

    def print_game_board(self):
        # This prints the game board contents
        print(self.Board.Grid)

    def reward_check(self, row, col):
        """
        This function is the alternative to sweep board, which sweeps the entire board and re-tallies the entire score.
        Instead this function should only check the piece currently placed and its surroundings
        :param row:
        :param col:
        :return:
        """
        int_blue_reward_tally = 0
        int_red_reward_tally = 0

        surrounding_pieces = self.get_surrounding_pieces(row, col)

        # First check if current piece is surrounded
        if self.piece_surrounded_alt(row, col, adjacent_pieces=surrounding_pieces):
            if self.Board.Grid[row, col] == Game.BLUE_PIECE:
                int_red_reward_tally += Game.POINT_REWARD
                self.PlayerTwoScore += 1
            elif self.Board.Grid[row, col] == Game.RED_PIECE:
                self.PlayerOneScore += 1
                int_blue_reward_tally += Game.POINT_REWARD

        # Now we check the adjacent pieces to see if they got surrounded
        for piece in surrounding_pieces:
            if self.Board.Grid[piece[0], piece[1]] == Game.EMPTY:
                continue
            elif self.piece_surrounded_alt(piece[0], piece[1]):
                if self.Board.Grid[piece[0], piece[1]] == Game.BLUE_PIECE:
                    int_red_reward_tally += Game.POINT_REWARD
                    self.PlayerTwoScore += 1
                elif self.Board.Grid[piece[0], piece[1]] == Game.RED_PIECE:
                    int_blue_reward_tally += Game.POINT_REWARD
                    self.PlayerOneScore += 1

        return [int_blue_reward_tally, int_red_reward_tally]

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
        Checks the empty_spots list. If its length is zero, the game is done, return true
        otherwise return false.
        :return: boolean. returns True if there are no empty spots left on the game board
        """
        if len(self.Board.empty_spots) > 0:
            return False
        else:
            # self.game_is_on = False
            return True

    def piece_surrounded_alt(self, row, col, adjacent_pieces=None):

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
        # These are the top, bottom, right and left pieces
        output = [[row-1, col], [row+1, col], [row, col+1], [row, col-1]]
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
