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

    def do_ai_move(self, arg_game_board_reference):
        """
        :param arg_game_board_reference: the current state of the game board
        :return: should return [row, col] indicating where to play next
        """
        # this is the master list of all strategies from which we can pull out different sub-strategies
        # and boardstate assessments
        master_list = Strategy.get_all_strategies(arg_game_board_reference, self.piece_color)

        # Create a sub-list of strategies which will cause the AI to win on the next move

        # Create a sub-list of strategies where AI must block its opponent from scoring

        # Create a sub-list of strategies that allow the AI to play moves that will lead it to a score a point

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

    def __init__(self, arg_game_board_reference, arg_center, arg_in_piece):

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

        self.is_white_space_block_opportunity = False
        self.white_space_block_priority = 0

        # Piece identification
        self.in_piece = arg_in_piece # Own piece
        self.out_piece = Strategy.get_opp_color(self.in_piece)

        # Calculate possible plays
        # print("strategy centered on", self.center)
        # print("length of surrounding tiles =", len(self.surrounding_tiles))
        # print("surrounding tiles index 0 is", self.surrounding_tiles[0])
        self.possible_moves = self.get_possible_moves(arg_game_board_reference, diagonals=False)
        self.possible_moves_diagonal = self.get_possible_moves(arg_game_board_reference, diagonals=True)

        # Determine white-space blocking status
        self.white_space_block_priority = self.determine_whitespace_block(arg_game_board_reference)

    @staticmethod
    def get_all_strategies(arg_game_board_reference, home_piece):
        """
        Returns a list of all strategies for a board state
        :param arg_game_board_reference: current board state
        :param home_piece: the piece color of the player (AI) getting the list of all strategies
        :return: list [] of all strategies
        """
        list_of_strategies = []  # Blank List of all possible strategies centered around a  at [rows, cols]

        if isinstance(arg_game_board_reference, GameBoard):
            for rows in range(0, len(arg_game_board_reference.Grid)):
                for cols in range(0, arg_game_board_reference.COL_COUNT):
                    s = Strategy(arg_game_board_reference, [rows, cols], home_piece)
                    list_of_strategies.append(s)  # Add the strategy to our list of strategies

            print("Total number of list_of_strategies", len(list_of_strategies))
        else:
            raise ValueError("Invalid gameboard state")

        return list_of_strategies

    @staticmethod
    def get_point_scoring_strategies(arg_raw_list, AIPiece):
        # go through the raw list and only
        pass

    def get_possible_moves(self, boardstate, diagonals=False):
        """
        :param diagonals: if true, func returns surrounding pieces on diagonals only.
        :param boardstate: reference to the gameboard
        :return:
        """
        return_list = []
        if diagonals:
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

    @staticmethod
    def contains_count_of(arg_list_of, target, arg_boardstate):
        """
        This static method returns the count of
        :param arg_list_of: an array of y,x co-ords
        :param arg_boardstate: refernce to the current gameboard state
        :param target: the piece color we are querying
        :return:
        """
        count = 0
        for index in range(0, len(arg_list_of)):
            row, col = arg_list_of[index]
            if arg_boardstate.Grid[row, col] == target:
                count += 1

        return count

    def determine_whitespace_block(self, arg_boardstate):
        """
        :param arg_boardstate: reference to the gameboard
        :return: integer representing the strategy priority -0 to 4 (4 being highest priority)
        """
        r_value = 0
        if self.piece_color_at_center == 0:
            if self.contains_count_of(self.surrounding_tiles, 0, arg_boardstate) > 0 and \
             self.contains_count_of(self.surrounding_tiles, self.in_piece, arg_boardstate) == 0:
                if self.contains_count_of(self.surrounding_tiles, self.out_piece, arg_boardstate) > 0:
                    r_value = 6 - len(self.possible_moves) - \
                     self.contains_count_of(self.possible_moves, 0, arg_boardstate)
                    self.is_white_space_block_opportunity = True
                    print("Debug: Saw white space block opportunity at ", self.center)

        return r_value

    def determine_point_block(self, arg_boardstate):
        """
        This determines whether the piece at center (one's own piece) is in the process of being surrounded, and
        determines a move that will block the opponent from scoring
        4 - Top priority - as in one move left until opponent scores
        3 - Two spots to score
        2 - Three spots to score
        1 - Four spots to score
        :param arg_boardstate:
        :return: void
        """
        aggressor = 0  # keep track of person who is trying to score
        row, col = self.center
        target_color_at_center = arg_boardstate.Grid[row, col]

        if not target_color_at_center == 0:
            aggressor = self.get_opp_color(target_color_at_center)
        else:
            # write it off
            self.is_block_opportunity = False
            self.block_priority_level = 0
            return

        # Evaluate the surrounding tiles
        if self.contains_count_of(self.surrounding_tiles, target_color_at_center, arg_boardstate) > 0 :
            # Abort as the defender has blocked the aggressor
            self.is_block_opportunity = False
            self.block_priority_level = 0
            return
        else:
            if self.contains_count_of(self.surrounding_tiles, 0, arg_boardstate) > 0:
                # Surrounding piece contains and empty space and not one of the defender's pieces
                self.is_block_opportunity = True
                self.block_defender_player = target_color_at_center
                self.block_priority_level = 5 - self.contains_count_of(self.surrounding_tiles, 0, arg_boardstate)

    @staticmethod
    def get_opp_color(arg_in_color):
        """

        :return: the opposite piece color to the player
        """
        if arg_in_color == 1:
            return 2
        elif arg_in_color == 2:
            return 1
        else:
            raise ValueError("Invalid piece color.")