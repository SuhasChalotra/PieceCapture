import gym
from gym_12x12.envs.env_classes.player import Player, HumanPlayer, BotPlayer, AgentPlayer
from gym_12x12.envs.env_classes.game import Game
from gym import spaces


class PlayerType:

    HUMAN = 2
    AGENT = 1
    BOT = 0


class gym12x12_env(gym.Env):

    def __init__(self):
        self.Game = None
        self.CurrentPlayer = None
        self.action_space = None
        self.observation_space = None

    def step(self, action):
        """
        This complies with the gym interface: Placing a tile on the board and alternates the current player
        :param action: a tuple  which contains the player's row_move, col_move -ie. where they will
         place the tile on the board(y, x)
        :return: observation, reward, done, info
        """
        agent_master_reward_tally = 0

        # Agent makes a play. move_results results in true or false
        move_results, p1_reward, p2_reward = self.Game.place_piece(self.CurrentPlayer, action[0], action[1])
        if self.CurrentPlayer.piece_color == Game.BLUE_PIECE:
            agent_master_reward_tally += p1_reward - p2_reward
        elif self.CurrentPlayer.piece_color == Game.RED_PIECE:
            agent_master_reward_tally += p2_reward - p1_reward

        done_flag = self.Game.is_game_complete()
        return_dict = []

        if not move_results:
            # We must abort the step function and return the reward_tally (which should be negative)
            return self.Game.Board.Grid, agent_master_reward_tally, done_flag, return_dict

        self.alternate_player()  # switch players

        # Make a non-agent move
        if not done_flag:
            ob_grid, p1r, p2r = self.make_non_agent_move()
            # Calculate reward - we're essentially subtracting the agent's opponent's reward from the agent's
            # reward, thereby calculating the net reward for the agent
            if self.CurrentPlayer.piece_color == Game.BLUE_PIECE:  # the non-agent is blue, subtract red from blue
                agent_master_reward_tally += p2r - p1r
            elif self.CurrentPlayer.piece_color == Game.RED_PIECE:  # the non-agent is red. subtract blue from red
                agent_master_reward_tally += p1r - p2r

            done_flag = self.Game.is_game_complete()

        self.alternate_player()  # again, we alternate the player
        return self.Game.Board.Grid, agent_master_reward_tally, done_flag, return_dict
        #  observations, rewards, done, info

    def render(self):
        self.Game.print_game_board()  # Prints the game board

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

        self.Game.Board.clear()
        self.CurrentPlayer = self.Game.Player1  # Player 1 always starts

        # If the current player (player1) is not Agent, then we call our make non-agent move function and
        # get an initial observation with the non-agent move
        if not isinstance(self.CurrentPlayer, AgentPlayer):
            # Call our make_non_agent_move method
            init_observation, p1r, p2r = self.make_non_agent_move()
            # Return an initial observation based on this move
            return init_observation

        else:
            # Essentially returning an empty board (and initial observation)
            return self.Game.Board.Grid

    def close(self):
        pass

    def seed(self, seed=None):
        pass

    def make_non_agent_move(self):
        """
        :return: observation and reward
        """
        if isinstance(self.CurrentPlayer, BotPlayer):
            # Check if it's bot
            move = BotPlayer.get_ai_move(self.Game.empty_spots)
            valid_m, p1_reward, p2_reward = self.Game.place_piece(self.CurrentPlayer, move[0], move[1])
            # self.alternate_player()

            # We need to return an obs and reward
            return self.Game.Board.Grid, p1_reward, p2_reward

        elif isinstance(self.CurrentPlayer, HumanPlayer):
            # go in some input loop ensuring the Human player's input is valid
            # self.alternate_player()

            pass

    @staticmethod
    def create_player(player_type, dumb_bot_ai=True):
        """
        :param dumb_bot_ai: Only applies to type Bot: True = use random move strategy, false = use smart AI algorithm
        :param player_type: Specify either a player or an AI
        :return: returns the requested player type
        """
        if player_type == PlayerType.HUMAN:

            return HumanPlayer()

        elif player_type == PlayerType.AGENT:

            return AgentPlayer()

        elif player_type == PlayerType.BOT:
            if dumb_bot_ai:
                return BotPlayer(True)
            else:
                return BotPlayer(False)

    def alternate_player(self):
        if self.CurrentPlayer == self.Game.Player1:
            self.CurrentPlayer = self.Game.Player2
        else:
            self.CurrentPlayer = self.Game.Player1

    def initiate_game(self, arg_player1, arg_player2, arg_int_boardsize):
        # When the game is initialized we
        if not isinstance(arg_player1, Player):
            raise ValueError("Player 1 must be a player")

        if not isinstance(arg_player2, Player):
            raise ValueError("Player 2 must be a player")

        self.Game = Game(arg_player1, arg_player2, rows=arg_int_boardsize, cols=arg_int_boardsize)
        self.CurrentPlayer = self.Game.Player1
        self.action_space = spaces.Discrete(arg_int_boardsize * arg_int_boardsize)
        self.observation_space = spaces.Box(high=-1000.0, low=1000.0, shape=[arg_int_boardsize, arg_int_boardsize], dtype=float)


