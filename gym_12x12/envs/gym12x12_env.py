import gym
from gym_12x12.envs.env_classes.player import Player, HumanPlayer, AIPlayer
from gym_12x12.envs.env_classes.game import Game

PLAYERTYPE_HUMAN = 0
PLAYERTYPE_AI = 1


class gym12x12_env(gym.Env):

    def __init__(self):
        self.Player1 = None
        self.Player2 = None
        self.Game = None
        self.CurrentPlayer = None

    def step(self, action):
        """
        This complies with the gym interface: Placing a tile on the board and alternates the current player
        :param action: a tuple  which contains the player's row_move, col_move -ie. where they will
         place the tile on the board(y, x)
        :return:
        """

        output = self.Game.place_piece(self.CurrentPlayer, action[0], action[1])
        if output == Game.GAME_MOVE_VALID:
            if self.CurrentPlayer == self.Player1:
                self.CurrentPlayer = self.Player2
            else:
                self.CurrentPlayer = self.Player1

        #Add a check for rewards

        #Return observations, rewards, done, info

    def render(self):
        self.Game.print_game_board()  # Prints the game board

    def reset(self, argPlayer1, argPlayer2, size_rows=12, size_cols=12):
        """
        Resets the fields. Defaults the current player to Player1
        :param argPlayer1: Player1
        :param argPlayer2: Player2
        :param size_rows: x size of game board (default = 12)
        :param size_cols: y size of game board (default = 12)
        :return:
        """
        self.Player1 = argPlayer1
        self.Player2 = argPlayer2
        self.Game = Game(self.Player1, self.Player2, size_y=size_rows, size_x=size_cols)
        self.CurrentPlayer = self.Player1

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
        else:
            return AIPlayer()


