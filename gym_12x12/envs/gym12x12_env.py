import gym
from gym_12x12.envs.env_classes.player import Player, HumanPlayer, BotPlayer, AgentPlayer
from gym_12x12.envs.env_classes.game import Game
from gym import spaces
import random as rnd
import pygame
import warnings

MARGIN = 5
BLOCK_SIZE = 30


class PlayerType:
    HUMAN = 2
    AGENT = 1
    BOT = 0


class gym12x12_env(gym.Env):
    GAME_TYPE_AGENT_V_BOT = 0
    GAME_TYPE_AGENT_V_HUMAN = 1
    GAME_TYPE_BOT_V_BOT = 2
    GAME_TYPE_BOT_V_HUMAN = 3

    def __init__(self):
        self.Game = None
        self.action_space = None
        self.observation_space = None
        self.AgentPlayer = None
        self.NonAgentPlayer = None
        self.screen = None
        self.GameType = None
        self.Render = False

    def step(self, action):
        """
        This complies with the gym interface: Placing a tile on the board and alternates the current player
        :param action: a tuple  which contains the player's row_move, col_move -ie. where they will
         place the tile on the board(y, x)
        :return: observation, reward, done, info
        """
        if self.GameType == self.GAME_TYPE_AGENT_V_BOT or self.GameType == self.GAME_TYPE_AGENT_V_HUMAN:
            agent_master_reward_tally = 0

            # Agent makes a play. move_results results in true or false
            move_results, p1_reward, p2_reward = self.Game.place_piece(self.AgentPlayer, (action[0], action[1]))
            if self.AgentPlayer.piece_color == Game.BLUE_PIECE:
                agent_master_reward_tally += p1_reward - p2_reward
            elif self.AgentPlayer.piece_color == Game.RED_PIECE:
                agent_master_reward_tally += p2_reward - p1_reward

            done_flag = self.Game.is_game_complete()
            return_dict = []

            if (not move_results) or done_flag:
                # We must abort the step function and return the reward_tally (which should be negative)
                return self.Game.Board.Grid, agent_master_reward_tally, done_flag, return_dict

            # Make a non-agent move
            if not done_flag:
                ob_grid, p1r, p2r = self.make_non_agent_move()
                # Calculate reward - we're essentially subtracting the agent's opponent's reward from the agent's
                # reward, thereby calculating the net reward for the agent
                if self.NonAgentPlayer.piece_color == Game.BLUE_PIECE:  # the non-agent is blue, subtract red from blue
                    agent_master_reward_tally += p2r - p1r
                elif self.NonAgentPlayer.piece_color == Game.RED_PIECE:  # the non-agent is red. subtract blue from red
                    agent_master_reward_tally += p1r - p2r

                done_flag = self.Game.is_game_complete()

            return self.Game.Board.Grid, agent_master_reward_tally, done_flag, return_dict
            #  observations, rewards, done, info
        else:
            # Game type is bot_v_human or bot_v_bot
            ob_grid, p1r, p2r = self.make_non_agent_move()
            done_flag = self.Game.is_game_complete()
            return self.Game.Board.Grid, 0, done_flag, []

    def render(self, mode='human'):
        self.draw_grid(self.Game.Board.Grid)
        pygame.event.get()
        pygame.display.flip()

    def reset(self):
        """
        :return: returns an initial observation
        """
        #  We will make sure that all of the required elements of the game are not null.
        #  Player objects must be propely instantiated, and
        #  the game properly initiated using the initiate_game method

        if self.Game is None or self.Game.Player1 is None or self.Game.Player2 is None:
            raise ValueError("Game not propely initiated. (Games or Players)")

        if self.action_space is None or self.observation_space is None:
            raise ValueError("Game not propely initiated. Check action or observation spaces")

        self.Game.reset()
        self.Game.start()

        # If Player1 is not Agent, then we call our make non-agent move function and
        # get an initial observation with the non-agent move
        if self.GameType == self.GAME_TYPE_AGENT_V_BOT or self.GameType == self.GAME_TYPE_AGENT_V_HUMAN:
            if not isinstance(self.Game.Player1, AgentPlayer):
                self.NonAgentPlayer = self.Game.Player1  # Assign non agent player
                self.AgentPlayer = self.Game.Player2  # Assign the agent
                # Call our make_non_agent_move method
                init_observation, p1r, p2r = self.make_non_agent_move()
                # Return an initial observation based on this move

                # self.alternate_player()
                # self.Game.print_game_board()
                return init_observation

            else:
                # Essentially returning an empty board (and initial observation)
                self.NonAgentPlayer = self.Game.Player2  # Assign non agent player
                self.AgentPlayer = self.Game.Player1  # Assign the agent
                # self.alternate_player()

                return self.Game.Board.Grid, 0, 0
        elif self.GameType == self.GAME_TYPE_BOT_V_HUMAN:
            # Bot V Human. This is a non-agent type scenario
            null_obs, p1r, p2r = self.make_non_agent_move()
            return null_obs
        elif self.GameType == self.GAME_TYPE_BOT_V_BOT:
            # implement a bot v bot scenario
            null_obs, p1r, p2r = self.make_non_agent_move()
            return null_obs
            raise NotImplemented("Not implemented yet")

    def close(self):
        pass

    def seed(self, seed=None):
        pass

    def get_smart_move(self, non_agent_player=None):
        if self.GameType == self.GAME_TYPE_AGENT_V_BOT:
            return self.NonAgentPlayer.get_ai_move(self.Game.Board)
        else:
            if isinstance(non_agent_player, BotPlayer):
                return non_agent_player.get_ai_move(self.Game.Board)
            else:
                raise ValueError("Get smart move...unable to determine non-agent-player")

    def get_dumb_move(self):
        """
        This function returns a random spot to play from the Game.Board.empty_spaces property
        :empty_move_list: the cached list of available moves
        :return: [row,col]
        """

        if len(self.Game.Board.empty_spots) > 0:
            choice = rnd.randint(0, len(self.Game.Board.empty_spots) - 1)
            return self.Game.Board.empty_spots[choice]
        else:
            return -1, -1  # Signifies that there are no empty moves left

    def make_non_agent_move(self):
        """
        :return: observation and reward
        """
        if self.GameType == self.GAME_TYPE_AGENT_V_BOT or self.GameType == self.GAME_TYPE_AGENT_V_HUMAN:
            if isinstance(self.NonAgentPlayer, BotPlayer):
                # Check if we're using smart or dumb strategies
                if not self.NonAgentPlayer.smart_ai:
                    move = self.get_dumb_move()
                else:
                    move = self.get_smart_move(non_agent_player=self.NonAgentPlayer)

                valid_m, p1_reward, p2_reward = self.Game.place_piece(self.NonAgentPlayer, (move[0], move[1]))

                # We need to return an obs and reward
                return self.Game.Board, p1_reward, p2_reward

            if isinstance(self.NonAgentPlayer, HumanPlayer):
                move = None

                while move is None:
                    self.render()
                    move = pygame.event.wait()
                    valid_m = Game.GAME_MOVE_INVALID

                    if move.type == pygame.MOUSEBUTTONDOWN:
                        y, x = move.pos
                        y, x = y // (MARGIN + BLOCK_SIZE), x // (MARGIN + BLOCK_SIZE)
                        valid_m, p1_reward, p2_reward = self.Game.place_piece(self.NonAgentPlayer, (x, y))

                    if not valid_m:
                        move = None

                    else:
                        return self.Game.Board, p1_reward, p2_reward
                pass
        elif self.GameType == self.GAME_TYPE_BOT_V_HUMAN:
            if isinstance(self.Game.Player1, HumanPlayer):
                move = None

                while move is None:
                    self.render()
                    move = pygame.event.wait()
                    valid_m = Game.GAME_MOVE_INVALID

                    if move.type == pygame.MOUSEBUTTONDOWN:
                        y, x = move.pos
                        y, x = y // (MARGIN + BLOCK_SIZE), x // (MARGIN + BLOCK_SIZE)
                        valid_m, p1_reward, p2_reward = self.Game.place_piece(self.Game.Player1, (x, y))

                    if not valid_m:
                        move = None

                    else:
                        # Bot move here
                        g_move = None
                        if self.Game.Player2.smart_ai:
                            g_move = self.get_smart_move(non_agent_player=self.Game.Player2)
                        else:
                            g_move = self.get_dumb_move()

                        valid_m, p1_reward, p2_reward = self.Game.place_piece(self.Game.Player2, g_move)
                        break

                return self.Game.Board.Grid, p1_reward, p2_reward
            elif isinstance(self.Game.Player1, BotPlayer):
                bot_move = None
                if self.Game.Player1.smart_ai:
                    bot_move = self.get_smart_move(non_agent_player=self.Game.Player1)
                else:
                    bot_move = self.get_dumb_move()

                # Do a bot move then enter a loop and get the human input
                valid_m, p1_reward, p2_reward = self.Game.place_piece(self.Game.Player1, bot_move) # TODO This code probably doesn't make sense
                p_move = None
                while p_move is None:
                    self.render()
                    p_move = pygame.event.wait()
                    valid_m = Game.GAME_MOVE_INVALID

                    if p_move.type == pygame.MOUSEBUTTONDOWN:
                        y, x = p_move.pos
                        y, x = y // (MARGIN + BLOCK_SIZE), x // (MARGIN + BLOCK_SIZE)
                        valid_m, p1_reward, p2_reward = self.Game.place_piece(self.Game.Player2, (x, y))

                    if not valid_m:
                        p_move = None
                    else:
                        break

                return self.Game.Board.Grid, p1_reward, p2_reward

        elif self.GameType == self.GAME_TYPE_BOT_V_BOT:
            # Player 1 and Player 2 are both bots
            p1_botmove = None
            p2_botmove = None
            valid_m = None
            p1_reward = None
            p2_reward = None

            # Get a move for player 1
            if self.Game.Player1.smart_ai:
                p1_botmove = self.get_smart_move(non_agent_player=self.Game.Player1)

            else:
                # Get a dumb, random move
                p1_botmove = self.get_dumb_move()

            # Player 1 shall make its move
            valid_m, p1_reward, p2_reward = self.Game.place_piece(self.Game.Player1, p1_botmove)

            # Get a move for player 2
            if self.Game.Player2.smart_ai:
                p2_botmove = self.get_smart_move(non_agent_player=self.Game.Player2)
            else:
                # Get a dumb move
                p2_botmove = self.get_dumb_move()

            valid_m, p1_reward, p2_reward = self.Game.place_piece(self.Game.Player2, p2_botmove)

            return self.Game.Board.Grid, p1_reward, p2_reward

    @staticmethod
    def create_player(player_type, argname, smart_ai=False):
        """
        :param smart_ai: Only applies to type Bot: True = Use smart AI (hard coded algo), false = use random move (dumb)
        :param player_type: Specify either a player or an AI
        :param argname: friendly name
        :return: returns the requested player type
        """
        if player_type == PlayerType.HUMAN:
            if smart_ai:
                warnings.warn("Smart AI is set to true, but will have no effect on an human player")
            return HumanPlayer()

        elif player_type == PlayerType.AGENT:
            if smart_ai:
                warnings.warn("Smart AI is set to true, but will have no effect on an agent player")
            return AgentPlayer(arg_name=argname)

        elif player_type == PlayerType.BOT:
            return BotPlayer(bot_name=argname, arg_smart_ai=smart_ai)

    def initiate_game(self, arg_player1, arg_player2, arg_int_boardsize, arg_game_type, arg_render=False):
        # When the game is initialized we validate the type of player supplied
        """
        :param arg_player1:
        :param arg_player2:
        :param arg_int_boardsize:
        :param arg_game_type:
        :return:
        """

        if not isinstance(arg_player1, Player):
            raise ValueError("Player 1 must be a player")

        if not isinstance(arg_player2, Player):
            raise ValueError("Player 2 must be a player")

        if isinstance(arg_player1, AgentPlayer) and isinstance(arg_player2, AgentPlayer):
            raise ValueError("Error. Two agents in game not allowed.")

        if not self.make_sure_players_must_be(arg_game_type, arg_player1, arg_player2):
            raise ValueError("Error. Game type is", arg_game_type, " but player types do not adhere to the game type")

        self.GameType = arg_game_type
        self.Game = Game(arg_player1, arg_player2, rows=arg_int_boardsize, cols=arg_int_boardsize)
        self.action_space = spaces.Discrete(arg_int_boardsize * arg_int_boardsize)
        self.Render = arg_render

        self.observation_space = spaces.Box(high=2, low=-1, shape=[arg_int_boardsize, arg_int_boardsize], dtype=int)

        # Initialize pygame and set Screen size
        if self.Render:
            pygame.init()
            screen_size = (MARGIN + BLOCK_SIZE) * arg_int_boardsize + MARGIN
            scoreboard_width = 150
            self.screen = pygame.display.set_mode((screen_size + scoreboard_width, screen_size)) # TODO - adjust dimensions to accomodate a small scoreboard. Add a scoreboard

            self.screen.fill((0, 0, 0))

    def make_sure_players_must_be(self, game_type, p1, p2):
        """
        This is a helper function that returns true if one of the players is of type_one, and the other is of type_two
        :param p1: a player
        :param p2: a second player
        :param game_type: an integer indicating the game type
        :return: bool
        """
        if game_type == self.GAME_TYPE_AGENT_V_BOT:
            if isinstance(p1, AgentPlayer) and isinstance(p2, BotPlayer):
                return True
            elif isinstance(p1, BotPlayer) and isinstance(p2, AgentPlayer):
                return True
            else:
                return False
        elif game_type == self.GAME_TYPE_AGENT_V_HUMAN:
            if isinstance(p1, AgentPlayer) and isinstance(p2, HumanPlayer):
                return True
            elif isinstance(p1, HumanPlayer) and isinstance(p2, AgentPlayer):
                return True
            else:
                return False
        elif game_type == self.GAME_TYPE_BOT_V_BOT:
            if isinstance(p1, BotPlayer) and isinstance(p2, BotPlayer):
                return True
            else:
                return False
        elif game_type == self.GAME_TYPE_BOT_V_HUMAN:
            if isinstance(p1, BotPlayer) and isinstance(p2, HumanPlayer):
                return True
            elif isinstance(p1, HumanPlayer) and isinstance(p2, BotPlayer):
                return True
            else:
                return False
        else:
            return False

    def from_int_to_tuple(self, arg_int):
        """
        Returns the array index to a [row, col] tuple
        :param arg_int: the index of an array
        :return: a tuple [row, col] (y, x)
        """
        row = arg_int // self.Game.Board.ROW_COUNT
        col = arg_int % self.Game.Board.ROW_COUNT
        return tuple([row, col])

    def draw_grid(self, grid):
        """
        :param grid: Game.Board.Grid (a numpy zeros)
        :return: None
        """

        for col in range(self.Game.Board.COL_COUNT):
            for row in range(self.Game.Board.ROW_COUNT):
                y = (MARGIN + BLOCK_SIZE) * col + MARGIN
                x = (MARGIN + BLOCK_SIZE) * row + MARGIN

                if (col, row) in self.Game.captured_pieces:
                    pygame.draw.rect(self.screen, (255, 255, 0), (x, y, BLOCK_SIZE, BLOCK_SIZE))
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255), (x, y, BLOCK_SIZE, BLOCK_SIZE))

                if grid[col, row] == Game.BLUE_PIECE:
                    pygame.draw.circle(self.screen, (0, 0, 255), (x + BLOCK_SIZE//2, y + BLOCK_SIZE//2), BLOCK_SIZE//2)

                elif grid[col, row] == Game.RED_PIECE:
                    pygame.draw.circle(self.screen, (255, 0, 0),  (x + BLOCK_SIZE//2, y + BLOCK_SIZE//2), BLOCK_SIZE//2)



