from abc import ABC, ABCMeta, abstractmethod
from random import randint
from gym_12x12.envs.env_classes.gameboard import GameBoard

# Games need players. But we should only be able to instantiate a HumanPlayer or an AIPlayer
# The Class 'Player' is abstract


class Player (ABC):
    """
    The player class represents participants in our game. They can be human players or AI players.
    This is an abstract class and cannot be instantiated.
    """
    __metaclass__ = ABCMeta

    # Private instance variable
    _p_piece_color = None
    _p_name = None  # holds the name or label/identifier

    @property
    def piece_color(self):
        return self._p_piece_color

    @piece_color.setter
    def piece_color(self, value):
        self._p_piece_color = value

    @property
    def name(self):
        return self._p_name

    @name.setter
    def name(self, value):
        self._p_name = value

    def get_opp_color(self):
        """

        :return: the opposite piece color to the player
        """
        if self.piece_color == 1:
            return 2
        elif self.piece_color == 2:
            return 1
        else:
            return 0 # Invalid

class HumanPlayer (Player):
    """
    A human player will be prompted to make its move via the keyboard input
    """
    def __init__(self):
        self.name = "Human"
        pass


class AgentPlayer (Player):

    def __init__(self):
        pass


class BotPlayer (Player):
    """
    An AI Player
    """
    def __init__(self):
        self.name = "Bot_Player"
        pass

    def get_strategies(self, arg_game_board_reference):
        """
        :param arg_game_board_reference: the current state of the game board
        :return: should return [row, col] indicating where to play next
        """
        if isinstance(arg_game_board_reference, GameBoard):
            list_of_strategies = []  # Blank List of all possible strategies centered around a  at [rows, cols]

            for rows in range(0, len(arg_game_board_reference.Grid)):
                for cols in range(0, arg_game_board_reference.COL_COUNT):
                    s = Strategy(arg_game_board_reference, [rows, cols])
                    list_of_strategies.append(s)  # Add the strategy to our list of strategies

            print("Total number of list_of_strategies", len(list_of_strategies))

            # Create a sub-list of strategies which will cause the AI to win on the next move

            # Create a sub-list of strategies where AI must block its opponent from scoring

            # Create a sub-list of strategies that allow the AI to play moves that will lead it to a score a point

        return list_of_strategies # Return a List

    def get_random_move(self, empty_move_list):
        """
        This function returns a random spot to play
        :empty_move_list: the cached list of available moves
        :return: [row,col]
        """
        if isinstance(empty_move_list, list):
            if len(empty_move_list) > 0:
                choice = randint(0, len(empty_move_list))
                return empty_move_list[choice]
            else:
                return -1, -1  # Signifies that there are no empty moves left

    def make_strategic_move(self):
        pass

    def will_move_endanger_player(self, move, board_ref):
        """

        :param move: [row, col] where the AI is thinking about moving
        :param board_ref reference to the game board
        :return: bool, true if AI plays piece at [row, col] where the next move its opponent makes will cause
        the opponent to score
        """
        opp_color = self.get_opp_color()
        if isinstance(move, list) or isinstance(move, tuple):
            # extract

            r, c = move

            if not board_ref.Grid[r, c] == 0:
                raise ValueError("Unable to evaluate, as the move in question is not on an empty space.")

            s_pieces = board_ref.get_surrounding_pieces(r, c, diagonals=False)
            if board_ref.get_count_of(opp_color, s_pieces) == len(s_pieces) - 1 and \
            board_ref.get_count_of(0, s_pieces) == 1:
                return True

            if board_ref.get_count_of(opp_color, s_pieces) == len(s_pieces):
                return True

        return False


class Strategy:
    """" Strategies are objects that contain info on possible moves the AI can make. When the game board state is
    scanned / evaluated by the AI, the AI will store-up some possible strategies and then determine 'possible_plays',
    which are simply [row, col] of where to place the next move

    priority_level = 0  # holds the strategy priority level
    center = ()  # a strategy centers around a center tile of which we get the surrounding tiles, it will be a tuple
    possible_plays = []  # this should be a list of x,y for possible plays in this strategy
    surrounding_tiles = []  # this should be a list of x,y co-ordinates (max 4, min 2) of tiles that surround the center
    """

    def __init__(self, arg_game_board_reference, arg_center):

        self.center = arg_center
        row, col = arg_center  # extract from the tuple
        self.piece_color_at_center = arg_game_board_reference.Grid[row, col]
        self.surrounding_tiles = arg_game_board_reference.get_surrounding_pieces(row, col, diagonals=False)
        self.surrounding_tiles_diagonal = arg_game_board_reference.get_surrounding_pieces(row, col, diagonals=True)

        # Score building properties
        self.score_building_priority_level = 0
        self.is_score_building_opp = False
        self.scoring_move = [-1, -1]  # set as the default to indicate no scoring move
        self.score_builder = 0  # this should be 1 or 2, representing a player, or 0 for no player
        self.scoring_player = 0  # should be either 1 or 2, or 0 if no player

        # Possible moves
        self.possible_moves = []  # a list of tuples containing possible plays (straight)
        self.possible_moves_diagonal = []  # diagonal
        self.tag = ""  # a general purpose string tag

        # Blocking properties
        self.is_block_opportunity = False
        self.block_priority_level = 0
        self.block_defender_player = 0  # should be 1 or 2 indicating the player, or 0 for no player (default)

        self.white_space_block_opportunity = False
        self.white_space_block_priority = 0

        # Calculate possible plays
        # print("strategy centered on", self.center)
        # print("length of surrounding tiles =", len(self.surrounding_tiles))
        # print("surrounding tiles index 0 is", self.surrounding_tiles[0])
        self.possible_moves = self.get_possible_moves(arg_game_board_reference, diagonals=False)
        self.possible_moves_diagonal = self.get_possible_moves(arg_game_board_reference, diagonals=True)

    @staticmethod
    def get_point_scoring_strategies(arg_raw_list, AIPiece):
        # go through the raw list and only
        pass

    def get_possible_moves(self, boardstate, diagonals=False):
        """
        :param argSurrounding_Pieces: the surrounding pieces
        :param boardstate: reference to the gameboard
        :return:
        """
        return_list = []
        if diagonals == False:
            for index in range(0, len(self.surrounding_tiles)):
                r, c = self.surrounding_tiles[index]
                if boardstate.Grid[r, c] == 0:
                    return_list.append(self.surrounding_tiles[index])

        else:
            for index in range(0, len(self.surrounding_tiles_diagonal)):
                r, c = self.surrounding_tiles_diagonal[index]
                if boardstate.Grid[r, c] == 0:
                    return_list.append(self.surrounding_tiles_diagonal[index])

        return return_list
