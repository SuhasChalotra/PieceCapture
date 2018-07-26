import gym
from gym_12x12.envs.env_classes.player import Player, HumanPlayer, BotPlayer, AgentPlayer
from gym_12x12.envs.env_classes.game import Game
from gym import spaces
import random as rnd
import pygame

MARGIN = 5
BLOCK_SIZE = 30


class PlayerType:
    HUMAN = 2
    AGENT = 1
    BOT = 0


class gym12x12_env(gym.Env):

    def __init__(self):
        self.Game = None
        self.action_space = None
        self.observation_space = None
        self.AgentPlayer = None
        self.NonAgentPlayer = None
        self.screen = None

    def step(self, action):
        """
        This complies with the gym interface: Placing a tile on the board and alternates the current player
        :param action: a tuple  which contains the player's row_move, col_move -ie. where they will
         place the tile on the board(y, x)
        :return: observation, reward, done, info
        """
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
            return self.Game.Board, agent_master_reward_tally, done_flag, return_dict

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

        return self.Game.Board, agent_master_reward_tally, done_flag, return_dict
        #  observations, rewards, done, info

    def render(self, mode='human'):
        self.draw_grid(self.Game.Board.Grid)
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
        if not isinstance(self.Game.Player1, AgentPlayer):
            self.NonAgentPlayer = self.Game.Player1  # Assign non agent player
            self.AgentPlayer = self.Game.Player2  # Assign the agent
            # Call our make_non_agent_move method
            init_observation, p1r, p2r = self.make_non_agent_move()
            # Return an initial observation based on this move
            print("Initial reset move ", self.NonAgentPlayer.name)
            # self.alternate_player()
            self.Game.print_game_board()
            return init_observation

        else:
            # Essentially returning an empty board (and initial observation)
            self.NonAgentPlayer = self.Game.Player2  # Assign non agent player
            self.AgentPlayer = self.Game.Player1  # Assign the agent
            # self.alternate_player()
            self.Game.print_game_board()
            return self.Game.Board, 0, 0

    def close(self):
        pass

    def seed(self, seed=None):
        pass

    def make_agent_move(self):
        """
        agent move will make a random move
        :return: observation and reward
        """

    def _get_random_empty_move(self):
        """
        This function returns a random spot to play from the Game.Board.empty_spaces property
        :empty_move_list: the cached list of available moves
        :return: [row,col]
        """

        if len(self.Game.Board.empty_move_list) > 0:
            choice = rnd(0, len(self.Game.Board.empty_move_list) - 1)
            return self.Game.Board.empty_move_list[choice]
        else:
            return -1, -1  # Signifies that there are no empty moves left

    def make_non_agent_move(self):
        """
        :return: observation and reward
        """
        if isinstance(self.NonAgentPlayer, BotPlayer):
            # Check if it's bot
            move = self.NonAgentPlayer.get_ai_move(self.Game.Board)
            valid_m, p1_reward, p2_reward = self.Game.place_piece(self.NonAgentPlayer, (move[0], move[1]))

            # We need to return an obs and reward
            return self.Game.Board, p1_reward, p2_reward

        if isinstance(self.NonAgentPlayer, HumanPlayer):
            move = None

            while move is None:
                move = pygame.event.wait()
                if move.type == pygame.MOUSEBUTTONDOWN:
                    x, y = move.pos // (MARGIN + BLOCK_SIZE)
                    valid_m, p1_reward, p2_reward = self.Game.place_piece(self.NonAgentPlayer, (x, y))

                if not valid_m:
                    move = None

                else:
                    return self.Game.Board, p1_reward, p2_reward
            pass

    @staticmethod
    def create_player(player_type, argname, dumb_bot_ai=True):
        """
        :param dumb_bot_ai: Only applies to type Bot: True = use random move strategy, false = use smart AI algorithm
        :param player_type: Specify either a player or an AI
        :param argname: friendly name
        :return: returns the requested player type
        """
        if player_type == PlayerType.HUMAN:

            return HumanPlayer()

        elif player_type == PlayerType.AGENT:

            return AgentPlayer(arg_name=argname)

        elif player_type == PlayerType.BOT:
            if dumb_bot_ai:
                return BotPlayer(bot_name=argname)
            else:
                return BotPlayer(bot_name=argname)

    def initiate_game(self, arg_player1, arg_player2, arg_int_boardsize):
        # When the game is initialized we
        if not isinstance(arg_player1, Player):
            raise ValueError("Player 1 must be a player")

        if not isinstance(arg_player2, Player):
            raise ValueError("Player 2 must be a player")

        self.Game = Game(arg_player1, arg_player2, rows=arg_int_boardsize, cols=arg_int_boardsize)
        self.action_space = spaces.Discrete(arg_int_boardsize * arg_int_boardsize)
        self.observation_space = spaces.Box(high=2, low=-1, shape=[arg_int_boardsize, arg_int_boardsize], dtype=int)

        # Initialize pygame and set Screen size
        pygame.init()
        screen_size = (MARGIN + BLOCK_SIZE)* arg_int_boardsize + MARGIN

        self.screen = pygame.display.set_mode((screen_size, screen_size))
        self.screen.fill((0, 0, 0))

    def draw_grid(self, grid):

        for col in range(self.Game.Board.COL_COUNT):
            pygame.event.get()
            for row in range(self.Game.Board.ROW_COUNT):
                y = (MARGIN + BLOCK_SIZE) * col + MARGIN
                x = (MARGIN + BLOCK_SIZE) * row + MARGIN

                if (col, row) in self.Game.captured_pieces:
                    pygame.draw.rect(self.screen, (0, 0, 0), (x, y, BLOCK_SIZE, BLOCK_SIZE))
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255), (x, y, BLOCK_SIZE, BLOCK_SIZE))

                if grid[col, row] == Game.BLUE_PIECE:
                    pygame.draw.circle(self.screen, (0, 0, 255), (x + BLOCK_SIZE//2, y + BLOCK_SIZE//2), BLOCK_SIZE//2)

                elif grid[col, row] == Game.RED_PIECE:
                    pygame.draw.circle(self.screen, (255, 0, 0),  (x + BLOCK_SIZE//2, y + BLOCK_SIZE//2), BLOCK_SIZE//2)

                pygame.event.get()




