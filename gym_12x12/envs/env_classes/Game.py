from gym_12x12.envs.env_classes import player
from gym_12x12.envs.env_classes import Gameboard
from gym_12x12.envs.env_classes.exceptions import BadArgumentException

class Game:
    # This starts a new game / session. It should be initialized w/ a Gameboard and two player
    # objects
    def __init__(self, arg_GameBoard: Gameboard, arg_Player1: player, arg_Player2: player):
        # Must ensure that the correct object type is passed as parameters
        if isinstance(arg_GameBoard, Gameboard):
            self._GameBoard = arg_GameBoard
        else:
            raise BadArgumentException("Type must be of type Gameboard")

        if isinstance(arg_Player1, player):
            self.Player1 = arg_Player1
        else:
            raise BadArgumentException("Type must be of type Player")

        if isinstance(arg_Player2, player):
            self.Player2 = arg_Player2
        else:
            raise BadArgumentException("Type must be of type Gameboard")

        return

    def assignPlayerPieceColor():
        # This method will ensure that the players have unique piece colors and should correct
        # the piece color assignment should it be invalid
        # We need to check if the Player1 and Player2 fields of the game are null.

        return

