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
            return 0  # Invalid


class HumanPlayer (Player):
    """
    A human player will be prompted to make its move via the keyboard input
    """
    def __init__(self):
        self.name = "Human"
        pass


class AgentPlayer (Player):

    def __init__(self, arg_name="default_agent"):
        self.name = arg_name


class BotPlayer (Player):
    """
    An AI Player
    """
    def __init__(self, dumb_bot=False, arg_name="default_bot"):
        """

        :param dumb_bot: when set to true, bot makes random moves instead of smart AI moves
        """
        self.name = arg_name
        self.enable_white_space_strategy = True  # for use in the bot AI logic
        self.dumb_bot_logic = dumb_bot

    def get_ai_move(self, arg_game_board_reference):
        """
        :param arg_game_board_reference: the current state of the game board
        :return: should return [row, col] indicating where to play next
        """

        # Let's first determine if this AI Bot instance has the dumb_bot_logic flag turned on (true)
        # which means it will pick a random move, instead of doing the smart AI logic (if false)
        if self.dumb_bot_logic:
            print("Dumb bot logic move made!")
            return self.get_random_element(arg_game_board_reference.empty_spots)

        # this is the master list of all strategies from which we can pull out different sub-strategies
        # and boardstate assessments

        master_list = Strategy.get_all_strategies(arg_game_board_reference, self.piece_color)

        # Create a sub-list of strategies which will cause the AI to win on the next move
        sl_point_scoring_strategies = self.get_ai_point_scoring_strategies(master_list)

        # Create a sub-list of strategies where AI must block its opponent from scoring
        sl_point_blocking_strategies = self.get_defensive_block_strategies(master_list)

        # Create sublist for defense against white_space_strategies
        sl_white_space_defense_strategies = self.get_white_space_defense_strats(master_list)

        # Create a sub-list of strategies that allow the AI to play moves that will lead it to a score a point
        sl_point_building_strategies = self.get_point_building_strats(master_list)

        # Create offensive white space
        sl_white_space_off = self.get_white_space_offensive_str(master_list, arg_game_board_reference)

        # remaining strategies (left overs)
        sl_rem_strats = self.get_remaining_strats(master_list)

        return_move = self.process_sub_strategies(sl_point_scoring_strategies, sl_point_blocking_strategies,
                                                  sl_white_space_defense_strategies, sl_point_building_strategies,
                                                  sl_white_space_off, sl_rem_strats, arg_game_board_reference)
        return return_move

    def process_sub_strategies(self, pt_scoring, pt_blocking, white_space_def, pt_build, off_ws_str,
                               remaining_str, board_state):
        """
        This is a helper function to sort out all the lists of different strategies
        :param pt_scoring: point scoring strategy
        :param pt_blocking: strategies that block opponent from scoring
        :param white_space_def: block opponent's white space
        :param pt_build: strategies that build scoring opportunities for Bot
        :param off_ws_str: build white-space strategy
        :param remaining_str: else
        :param board_state: board state
        :return: [row, col] move

        """
        strat_return_move = [-1, -1]

        # 1) Determine point scoring strategies
        if len(pt_scoring) > 0:
            try_count = 0
            while True:
                if try_count >= board_state.board_size:
                    break

                int_pick = randint(0, len(pt_scoring) - 1)
                strat_return_move = pt_scoring[int_pick].scoring_move

                if not self.will_move_endanger_player(strat_return_move, board_state):
                    print("Point scoring strategy taken")
                    return strat_return_move
                else:
                    try_count += 1

        # 2) Determine point blocking strategies (block opponent from making next move that scores)
        if len(pt_blocking) > 0:
            L4, L3, L2 = self.extract_blocking_strategies(pt_blocking, self.piece_color)  # extract all levels blocking
            # the higher the level, the greater the priority. Pick a random strategy and random possible move from
            # the chosen strategy and return that
            if len(L4) > 0:
                int_pick = randint(0, len(L4) - 1)
                r_pick = randint(0, len(L4[int_pick].possible_moves) - 1)
                strat_return_move = L4[int_pick].possible_moves[r_pick]
                print("Lvl 4 Point block strategy taken")
                return strat_return_move

            if len(L3) > 0:
                int_pick = randint(0, len(L3) - 1)
                r_pick = randint(0, len(L3[int_pick].possible_moves) - 1)
                strat_return_move = L3[int_pick].possible_moves[r_pick]
                print("Lvl 3 Point block strategy taken")
                return strat_return_move

            if len(L2) > 0:
                int_pick = randint(0, len(L2) - 1)
                r_pick = randint(0, len(L2[int_pick].possible_moves) - 1)
                strat_return_move = L2[int_pick].possible_moves[r_pick]
                print("Lvl 2 Point block strategy taken")
                return strat_return_move

        # 3) White space defensive block strategies
        if len(white_space_def) > 0:
            for strat in white_space_def:
                if strat.white_space_block_priority >= 4:
                    # anaylze possible moves and make sure they don't endanger the Bot Player
                    int_count = 0
                    while True:
                        if int_count >= len(strat.possible_moves) + 5:
                            break

                        int_pick = randint(0, len(strat.possible_moves) - 1)
                        list_considered_move = strat.possible_moves[int_pick]

                        if not self.will_move_endanger_player(list_considered_move, board_state):
                            print("White space defensive block strategy chosen")
                            return list_considered_move
                        else:
                            int_count += 1

        # 4) Point scoring-build strategies
        if len(pt_build) > 0:
            if self.enable_white_space_strategy:
                if len(white_space_def) > 0:
                    # we should make sure we check for any white space
                    selected_advanced_strategies = []
                    for str_w_space in white_space_def:
                        # proritize white space strategies already in play
                            if Strategy.contains_count_of(str_w_space.surrounding_tiles_diagonal, self.piece_color,
                                                          board_state) > 0 and \
                                   Strategy.contains_count_of(str_w_space, self.piece_color, board_state) < \
                                   len(str_w_space.surrounding_tiles_diagonal) and \
                                   Strategy.contains_count_of(str_w_space.surrounding_tiles_diagonal, 0, board_state) > 0:
                                selected_advanced_strategies.append(str_w_space)

                    # check the newly-formed list and make sure it's greater than zero
                    if len(selected_advanced_strategies) > 0:
                        int_high_count = 1
                        int_target_index = -1
                        int_c = 0
                        # choose the highest
                        for _s in selected_advanced_strategies:
                            if Strategy.contains_count_of(_s.surrounding_tiles_diagonal, self.piece_color, board_state) > int_high_count:
                                int_high_count = Strategy.contains_count_of(_s.surrounding_tiles_diagonal, self.piece_color, board_state)
                                int_target_index = int_c

                            int_c += 1

                        if int_target_index >= 0:
                            ws_return_move = self.get_random_element(selected_advanced_strategies[int_target_index].possible_moves_diagonal)
                            print("White space advanced off strategy chosen")
                            return ws_return_move

            # No advanced white space strategies were found, so continue on with point building strategies
            # Extract and sort out the strategies by point_building priority level
            L4, L3, L2 = self.extract_point_building_strategies(pt_build, self.piece_color)

            if len(L4) > 0:
                int_count_break = 0
                while True:
                    if int_count_break >= len(board_state.empty_spots):
                        break

                    int_pb_pick = randint(0, len(L4) - 1)
                    move_choice = self.get_random_element(L4[int_pb_pick].possible_moves) # this is a tuple
                    # make sure the move won't endanger the AI
                    if not self.will_move_endanger_player(move_choice, board_state) and not self.will_move_spoil_white_space_strat(move_choice, board_state):
                        print("Level 4 Point building strategy taken")
                        return move_choice
                    else:
                        int_count_break += 1

            if len(L3) > 0:
                int_count_break = 0
                while True:
                    if int_count_break >= len(board_state.empty_spots):
                        break

                    int_pb_pick = randint(0, len(L3) - 1)
                    move_choice = self.get_random_element(L3[int_pb_pick].possible_moves)  # this is a tuple
                    # make sure the move won't endanger the AI
                    if not self.will_move_endanger_player(move_choice, board_state) and not self.will_move_spoil_white_space_strat(move_choice, board_state):
                        print("Level 3 Point building strategy taken")
                        return move_choice
                    else:
                        int_count_break += 1

            if len(L2) > 0:
                int_count_break = 0
                while True:
                    if int_count_break >= len(board_state.empty_spots):
                        break

                    int_pb_pick = randint(0, len(L2) - 1)
                    move_choice = self.get_random_element(L2[int_pb_pick].possible_moves)  # this is a tuple
                    # make sure the move won't endanger the AI
                    if not self.will_move_endanger_player(move_choice, board_state) and not self.will_move_spoil_white_space_strat(move_choice, board_state):
                        print("Level 2 Point building strategy taken")
                        return move_choice
                    else:
                        int_count_break += 1

        # Finally we check remaining strategies
        """
        At this point no viable strategies have been found (it's probably close to the end of the game. Let's sort out the remaining strategies and get the ones where there are 
        possible moves to play. Let's randomly pick
        """
        if len(remaining_str) > 0:
            int_count = 0
            while True:
                if int_count > len(board_state.empty_spots) - 1:
                    break

                strategy_chosen = self.get_random_element(remaining_str)  # get a random strategy

                for possible_move_option in strategy_chosen.possible_moves:
                    if not self.will_move_endanger_player(possible_move_option, board_state):
                        return possible_move_option

                int_count += 1

            # if all else fails, we must pick a random empty spot
            return self.get_random_element(board_state.empty_spots)
        else:
            return self.get_random_element(board_state.empty_spots)

        return strat_return_move  # if this is [-1, -1] then there are literally no more spots left, game should complete

    def extract_blocking_strategies(self, master_block_list, defender):
        """
        returns three lists list of level 4, 3, 2 block priorities
        :param master_block_list:
        :param defender: piece color being attacked. Cannot be empty
        :return: level4_List[], level3_List[], level2_List[]
        """
        level_4_list = []
        level_3_list = []
        level_2_list = []

        for strat in master_block_list:
            if strat.block_priority_level == 4 and strat.block_defender_player == defender:
                level_4_list.append(strat)
            elif strat.block_priority_level == 3 and strat.block_defender_player == defender:
                level_3_list.append(strat)
            elif strat.block_priority_level == 3 and strat.block_defender_player == defender:
                level_2_list.append(strat)

        return level_4_list, level_3_list, level_2_list

    def extract_point_building_strategies(self, master_pb_list, arg_int_builder):
        """
        returns three lists lists of level 4, 3, 2 point building priorities
        :param master_pb_list: the pre-filtered list of point blocking strategies
        :param arg_int_builder: the player building the scoring opp
        :return: List of List containing Level 4, 3, 2 strategies
        """
        level_4_list = []
        level_3_list = []
        level_2_list = []

        for strat in master_pb_list:
            if strat.is_score_building_opp:
                if strat.score_builder == arg_int_builder:
                    if strat.score_building_priority_level == 4:
                        level_4_list.append(strat)
                    elif strat.score_building_priority_level == 3:
                        level_3_list.append(strat)
                    elif strat.score_building_priority_level == 2:
                        level_2_list.append(strat)

        return level_4_list, level_3_list, level_2_list

    def get_random_element(self, empty_move_list):
        """
        This function returns a random spot to play
        :empty_move_list: the cached list of available moves
        :return: [row,col]
        """
        if isinstance(empty_move_list, list) or isinstance(empty_move_list, tuple):
            if len(empty_move_list) > 0:
                choice = randint(0, len(empty_move_list) - 1)
                return empty_move_list[choice]
            else:
                return -1, -1  # Signifies that there are no empty moves left

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
    def will_move_spoil_white_space_strat(self, move, boardref):
        """
        This evaluates if the next move will cancel out (spoil) a white space hole /trap. The AI shoudn't spoil its own white space strategies
        :param move: [row, col] a move
        :param boardref: reference to the current state of the gameboard
        :return: bool
        """
        if not isinstance(boardref, GameBoard):
            raise ValueError("Invalid gameboard reference")

        if not isinstance(move, list) and not isinstance(move, tuple):
            raise ValueError("Move parameter must be a tuple or list of coordinates [row, col]")


        # first we get the surrounding piecs
        row, col = move
        sur_pieces = boardref.get_surrounding_pieces(row, col)

        if Strategy.contains_count_of(sur_pieces, self.piece_color, boardref) == len(sur_pieces):
            return True

        return False

    def get_ai_point_scoring_strategies(self, master_list_source):
        """

        :param master_list_source:
        :return:
        """
        # Validation - make sure master list is of type list
        if not isinstance(master_list_source, list):
            raise ValueError("Parameter master_list_source must be of type list")

        if not all(isinstance(element, Strategy) for element in master_list_source):
            raise ValueError("Issues with master_list_source as not all elements are of type 'Strategy'")

        return_list = []

        for strategy in master_list_source:
            if strategy.scoring_player == self.piece_color:
                return_list.append(strategy)

        return return_list

    def get_defensive_block_strategies(self, master_list_source):
        """

        :param master_list_source:
        :return:
        """
        # Validation
        if not isinstance(master_list_source, list):
            raise ValueError("Parameter master_list_source must be of type list")

        if not all(isinstance(element, Strategy) for element in master_list_source):
            raise ValueError("Issues with master_list_source as not all elements are of type 'Strategy'")

        return_list = []
        for strategy in master_list_source:
            if strategy.block_priority_level >= 2 and strategy.is_block_opportunity \
               and strategy.block_defender_player == self.piece_color:
                return_list.append(strategy)

        return return_list

    def get_white_space_defense_strats(self, master_list):
        """

        :param master_list:
        :return:
        """
        if not isinstance(master_list, list):
            raise ValueError("Parameter must be of type list")

        return_list = []
        for strategy in master_list:
            if strategy.is_white_space_block_opportunity == True and strategy.white_space_block_priority >= 2:
                return_list.append(strategy)

        return return_list

    def get_white_space_offensive_str(self, master_list, board_state):
        """
        This is where we search for white space building strategies
        :param master_list:
        :param board_state:
        :return: a list of strategies
        """
        if not isinstance(master_list, list):
            raise ValueError("master_list must be of type list")

        opp_color = self.get_opp_color()
        return_list = []
        for strategy in master_list:
            if strategy.piece_color_at_center == 0 or strategy.piece_color_at_center == self.piece_color:
                if Strategy.contains_count_of(strategy.surrounding_tiles_diagonal, opp_color, board_state) \
                   > 0 or Strategy.contains_count_of(strategy.surrounding_tiles_diagonal, 0, board_state) == 0:
                    continue
                else:
                    return_list.append(strategy)

        return return_list

    def get_point_building_strats(self, master_list):
        """

        :param master_list:
        :return:
        """
        if not isinstance(master_list, list):
            raise ValueError("Needs to be of type list")
        return_list = []

        for strategy in master_list:
            if strategy.score_builder == self.piece_color:
                return_list.append(strategy)

        return return_list

    def get_remaining_strats(self, master_list):
        if not isinstance(master_list, list):
            raise ValueError("master list must be of type list")
        return_list = []
        for strategy in master_list:
            if len(strategy.possible_moves) > 0:
                return_list.append(strategy)

        return return_list


class Strategy:
    """" Strategies are objects that contain info on possible moves the AI can make. When the game board state is
    scanned / evaluated by the AI, the AI will store-up some possible strategies and then determine 'possible_plays',
    which are simply [row, col] of where to place the next move

    priority_level = 0  # holds the strategy priority level
    center = ()  # a strategy centers around a center tile of which we get the surrounding tiles, it will be a tuple
    possible_plays = []  # this should be a list of x,y for possible plays in this strategy
    surrounding_tiles = []  # this should be a list of [y,x] co-ordinates (max 4, min 2) of tiles that surround the
    center
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

        # Determine blocking
        self.determine_point_block(arg_game_board_reference)

        # Determine if there is a scoring opportunity on next move
        self.determine_point_scoring_move(arg_game_board_reference)

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

    def get_possible_moves(self, boardstate, diagonals=False):
        """
        :param diagonals: if true, func returns surrounding pieces on diagonals only.
        :param boardstate: reference to the gameboard
        :return:
        """
        return_list = []
        if not diagonals:
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

    def determine_whitespace_block(self, arg_boardstate):
        """
        :param arg_boardstate: reference to the gameboard
        :return: integer representing the strategy priority: 0 to 4 (4 being highest priority)
        """
        r_value = 0
        if self.piece_color_at_center == 0:
            if self.contains_count_of(self.surrounding_tiles, 0, arg_boardstate) > 0 and self.contains_count_of(self.surrounding_tiles, self.in_piece, arg_boardstate) == 0:
                if self.contains_count_of(self.surrounding_tiles, self.out_piece, arg_boardstate) > 0:
                    r_value = 6 - len(self.possible_moves) - self.contains_count_of(self.possible_moves, 0, arg_boardstate)
                    self.is_white_space_block_opportunity = True

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
        row, col = self.center  # extract row, col
        target_color_at_center = arg_boardstate.Grid[row, col]  # Get the piece color a the center (target)

        if not target_color_at_center == 0:
            #  if the piece color at center isn't 'empty', then we can get the opposite color (1 -> 2, 2 -> 1)
            aggressor = self.get_opp_color(target_color_at_center)
        else:
            # write it off as not an opportunity
            self.is_block_opportunity = False
            self.block_priority_level = 0
            return

        # Evaluate the surrounding tiles
        if self.contains_count_of(self.surrounding_tiles, target_color_at_center, arg_boardstate) > 0:
            # Abort as the defender has blocked the aggressor
            self.is_block_opportunity = False
            self.block_priority_level = 0
            return
        else:
            if self.contains_count_of(self.surrounding_tiles, 0, arg_boardstate) > 0:
                # Surrounding piece contains and empty space and not one of the defender's pieces
                self.is_block_opportunity = True
                # print('Blocking status is true centered around', self.center)
                self.block_defender_player = target_color_at_center
                self.block_priority_level = 5 - self.contains_count_of(self.surrounding_tiles, 0, arg_boardstate)

    def determine_point_scoring_move(self, arg_boardstate):
        """
        This will populate the object properties scoring_player and scoring_move
        :param arg_boardstate:
        :return: void
        """
        row, col = self.center  # extract the [y,x] of the center

        if not arg_boardstate.Grid[row, col] == 0:  # if not empty
            opposite_color_at_center = self.get_opp_color(arg_boardstate.Grid[row, col])
            if self.contains_count_of(self.surrounding_tiles, opposite_color_at_center, arg_boardstate) == \
               len(self.surrounding_tiles) - 1:
                # get a list of tuples containing empty
                output = self.get_tuples_containing(self.surrounding_tiles, 0, arg_boardstate)

                if len(output) == 1:
                    self.scoring_player = self.get_opp_color(arg_boardstate.Grid[row, col])
                    self.scoring_move = output[0]
        else:
            # No scoring move or scoring player for this strategy
            self.scoring_move = [-1, -1]
            self.scoring_player = 0

    def determine_score_building_strategies(self, arg_boardstate):
        # This method will populate the score building properties based on the center [row, col]
        opp_color = self.get_opp_color(self.piece_color_at_center)
        if self.piece_color_at_center == 0:
            # color at center is empty (0)
            self.score_builder = 0
            self.is_score_building_opp = False
            self.score_building_priority_level = 0
            self.tag = "not a score building chance"
            return

        # point building strategies that have been spoiled (ie., when one of the surrounding piece is the same
        # as the piece_at_center
        if self.contains_count_of(self.surrounding_tiles, self.piece_color_at_center, arg_boardstate) > 0:
            # not a good point-building strategy
            self.score_builder = 0
            self.is_score_building_opp = False
            self.score_building_priority_level = 0
            self.tag = "not a score-building chance as it has been blocked"
            return

        # A score building opportunity exists if there are >= 0 white spaces in the surrounding pieces
        # but one less than the surrounding_piece length
        if self.contains_count_of(self.surrounding_tiles, 0, arg_boardstate) > 0 and \
           self.contains_count_of(self.surrounding_tiles, opp_color, arg_boardstate) < len(self.surrounding_tiles):
            self.score_builder = opp_color
            self.is_score_building_opp = True
            self.score_building_priority_level = 6 - self.contains_count_of(self.surrounding_tiles, 0, arg_boardstate)
            return

    @staticmethod
    def contains_count_of(arg_list_of, target, arg_boardstate):
        """
        This static method returns the count of target within a given set arg_list_of
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

    @staticmethod
    def get_tuples_containing(arg_list_of, target, arg_boardstate):
        """
        This will return a list of [row, col] where piece color 'target' is found on the game board corresponding
        to [row, col] found in arg_list_of
        :param arg_list_of: a list[] of tuples [row, col]
        :param target: piece color (0, 1 or 2)
        :param arg_boardstate: reference to the current state of the gameboard
        :return: a list of tuples whose coordinates correspond to 'target' on the game board
        """
        # Validation
        if not isinstance(arg_list_of, list):
            raise ValueError("Invalid argument: argument 'arg_list_of' is not of type 'list' or 'tuple")

        if not isinstance(target, int):
            raise ValueError("Invalid argument: argument 'target' is not of type 'int'")

        if not isinstance(arg_boardstate, GameBoard):
            raise ValueError("Invalid argument: argument 'arg_boardstate is not of type 'Gameboard'")

        # This will be our return value
        return_list = []
        for item in arg_list_of:
            row, col = item
            if arg_boardstate.Grid[row, col] == target:
                return_list.append(item)

        return return_list

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
