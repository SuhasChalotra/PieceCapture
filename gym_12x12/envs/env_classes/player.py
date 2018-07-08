from abc import ABC, ABCMeta, abstractmethod
from random import randint

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


class HumanPlayer (Player):
    """
    A human player will be prompted to make its move via the keyboard input
    """
    def __init__(self):
        pass


class AgentPlayer (Player):

    def __init__(self):
        pass


class BotPlayer (Player):
    """
    An AI Player
    """
    def __init__(self):
        pass

    def get_strategies(self, arg_game_board_reference):
        """
        :param gamedata: the current game board
        :return: should return [row, col] indicating where to play next
        """

        list_of_strategies = []  # Blank List of all possible strategies centered around a piece

        for rows in range(0, len(arg_game_board_reference.Grid)):
            for cols in range(0, arg_game_board_reference.COL_COUNT):
                s = Strategy(arg_game_board_reference, [rows, cols])
                list_of_strategies.append(s)  # Add

        print("Total number of list_of_strategies", len(list_of_strategies))

        # Create a list of strategies which will cause the AI to win on the next move

        # Create a list of strategies where AI must block its opponent from scoring

        # Create a list of strategies that allow the AI to get a point

        return list_of_strategies # Return a List

    def make_random_move(self, empty_move_list):
        """
        This function returns a random spot to play
        :empty_move_list: the cached list of available moves
        :return: [row,col]
        """
        if isinstance(empty_move_list, list):
            choice = randint(0, len(empty_move_list))
            return empty_move_list.pop(choice)

    def make_strategic_move(self, empty_move_list):
        pass


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
        # self.Game = arg_game_reference  # This basically holds a reference to the current gameboard
        self.center = arg_center
        row, col = arg_center  # extract from the tuple
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
        self.block_defender = 0  # should be 1 or 2 indicating the player, or 0 for no player (default)

        # Calculate possible plays
        # print("strategy centered on", self.center)
        # print("length of surrounding tiles =", len(self.surrounding_tiles))
        # print("surrounding tiles index 0 is", self.surrounding_tiles[0])
        for piece in range(0, len(self.surrounding_tiles)):
            r, c = self.surrounding_tiles[piece]
            if arg_game_board_reference.Grid[r, c] == 0:  # Only add a possible play if the [r,c] is empty (0)
                self.possible_moves.append([r, c])


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
