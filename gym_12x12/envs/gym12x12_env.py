import gym
from gym_12x12.envs.env_classes.player import Player, HumanPlayer, BotPlayer, AgentPlayer
from gym_12x12.envs.env_classes.game import Game
from gym import spaces

PLAYERTYPE_HUMAN = 2
PLAYERTYPE_AGENT = 1
PLAYERTYPE_BOT = 0

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
        :return:
        """

        output = self.Game.place_piece(self.CurrentPlayer, action[0], action[1])
        if output == Game.GAME_MOVE_VALID:
            if self.CurrentPlayer == self.Game.Player1:
                self.CurrentPlayer = self.Game.Player2
            else:
                self.CurrentPlayer = self.Game.Player1

        #Add a check for rewards

        #Return observations, rewards, done, info

    def render(self):
        self.Game.print_game_board()  # Prints the game board

    def reset(self):
        """
        self, argPlayer1, argPlayer2, size_rows=12, size_cols=12
        Resets the fields. Defaults the current player to Player1
        :param argPlayer1: Player1
        :param argPlayer2: Player2
        :param size_rows: x size of game board (default = 12)
        :param size_cols: y size of game board (default = 12)
        :return:
        """

        self.Game.Board.clear()
        self.CurrentPlayer = self.Game.Player1

        #If the player 1 is a bot that is supposed to make a move it does so in reset
        if isinstance(BotPlayer, self.Game.Player1):
            move = BotPlayer.make_random_move(self.Game.empty_spots)
            self.Game.place_piece(self.CurrentPlayer,move[0], move[1])
        return self.Game.Board.Grid

        # self.Game.Board.Grid.

    def close(self):
        pass

    def seed(self, seed=None):
        pass

    @staticmethod
    def create_player(player_type):
        """
        :param player_type: Specify either a player or an AI
        :return: returns the requested player type
        """
        if player_type == PLAYERTYPE_HUMAN:

            return HumanPlayer()

        elif player_type == PLAYERTYPE_AGENT:

            return AgentPlayer()

        elif player_type == PLAYERTYPE_BOT:

            return BotPlayer()

    def initiate_game(self, arg_player1, arg_player2, arg_int_boardsize):

        self.Game = Game(arg_player1, arg_player2, rows=arg_int_boardsize, cols=arg_int_boardsize)
        self.CurrentPlayer = self.Player1
        self.action_space = spaces.Discrete(arg_int_boardsize * arg_int_boardsize)
        self.observation_space = spaces.Box(3, arg_int_boardsize, arg_int_boardsize)


