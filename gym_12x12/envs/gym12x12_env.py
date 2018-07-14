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

        move_results = self.Game.place_piece(self.CurrentPlayer, action[0], action[1])
        # The above MUST be agent's action and it must be Player1
        # we need a variable that keeps track of the reward for this immediate action in order to subtract it
        # later, depending on the BOT/Human move in response

        done_flag = self.Game.is_game_complete()
        info_tag = ""
        if move_results == Game.GAME_MOVE_VALID:
            if self.CurrentPlayer == self.Game.Player1:
                self.CurrentPlayer = self.Game.Player2

                # The move is valid; we need to do some calc for rewards

                if isinstance(self.CurrentPlayer, BotPlayer):
                    # Bot Player, bot makes a move
                    bot_move = BotPlayer.make_random_move(self.Game.empty_spots)
                    self.Game.place_piece(self.CurrentPlayer, bot_move)

                    # If the BOT scores, we need to do some calulation
                    self.CurrentPlayer = self.Game.Player1

                elif isinstance(self.CurrentPlayer, HumanPlayer):
                    # Do something, but not implemented
                    self.CurrentPlayer = self.Game.Player1
                    raise NotImplemented
                else:
                    raise ValueError("Invalid Player.")
            else:
                # This case should never evaluate to true, if so there is a problem w/ code:
                raise ValueError("This case should never evaluate to true as Player1 must be agent. Check code.")
        else:
            # The AIPlayer should be negatively rewarded for an invalid move. We should do this in the return value
            # of make_move
            # The BotPlayer should make its move and return the updated board state
            info_tag = "Agent penalized for making invalid move."
            if self.CurrentPlayer == self.Game.Player1:
                self.CurrentPlayer = self.Game.Player2
                # The bot or human player must make a move in response here
            else:
                # This case should never evaluate to true, if so there is a problem w/ code:
                raise ValueError("This case should never evaluate to true as Player1 must be agent. Check code.")
            return self.Game.Board.Grid, -1, done_flag, info_tag

        # Add a check for rewards

        #  observations, rewards, done, info

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

        #  We will make sure that all of the required elements of the game are not null.
        #  Player objects must be propely instantiated, and
        #  the game properly initiated using the initiate_game method

        if self.Game is None or self.Game.Player1 is None or self.Game.Player2 is None:
            raise ValueError("Game not propely initiated. (Games or Players)")

        if self.action_space is None or self.observation_space is None:
            raise ValueError("Game not propely initiated. Check action or observation spaces")

        self.Game.Board.clear()
        self.CurrentPlayer = self.Game.Player1  # Player 1 always starts

        info_tag = "first_move"

        # If the player 1 is a bot that is supposed to make a move it does so in reset
        if isinstance(self.Game.Player1, BotPlayer):
            move = BotPlayer.make_random_move(self.Game.empty_spots)
            self.Game.place_piece(self.CurrentPlayer, move[0], move[1])
        elif isinstance(self.Game.Player1, HumanPlayer):
            raise NotImplemented

        return self.Game.Board.Grid, 0, False, info_tag # return initial observation

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
        if not isinstance(arg_player1, AgentPlayer):
            raise ValueError("Player 1 must be an agent")

        if isinstance(arg_player2, AgentPlayer):
            raise ValueError("Player two must be a bot or a human. It cannot be an agent")

        self.Game = Game(arg_player1, arg_player2, rows=arg_int_boardsize, cols=arg_int_boardsize)
        self.CurrentPlayer = self.Player1
        self.action_space = spaces.Discrete(arg_int_boardsize * arg_int_boardsize)
        self.observation_space = spaces.Box(3, arg_int_boardsize, arg_int_boardsize)


