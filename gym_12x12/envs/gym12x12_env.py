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
        This complies with the gym interface: Placing a tile on the board and alternate the current player
        :param action: an ActionClass object which contains the player making the move and the x, y moves
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

    def reset(self, argPlayer1, argPlayer2, size_x=12, size_y=12):
        """
        Resets the fields. Defaults the current player to Player1
        :param argPlayer1: Player1
        :param argPlayer2: Player2
        :param size_x: x size of game board (default = 12)
        :param size_y: y size of game board (default = 12)
        :return:
        """
        self.Player1 = argPlayer1
        self.Player2 = argPlayer2
        self.Game = Game(self.Player1, self.Player2, arg_size_x=size_x, arg_size_y=size_y)
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

            return HumanPlayer(Game.BLUE)
        else:
            return AIPlayer(Game.RED)


