from abc import ABC, ABCMeta, abstractmethod
from gym_12x12.envs.env_classes.Gameboard import GameBoard, PieceColor

# Games need players. But we should only be able to instantiate a HumanPlayer or an AIPlayer
# The Class 'Player' is abstract


class Player (ABC):
    __metaclass__ = ABCMeta

    # Private instance variable
    _p_piece_color = None

    @property
    def piece_color(self):
        return self._p_piece_color

    @piece_color.setter
    def piece_color(self, value):
        self._p_piece_color = value


class HumanPlayer (Player):
    def __init__(self, arg_piece_color: PieceColor):
        self.piece_color = arg_piece_color


class AIPlayer (Player):
    def __init__(self, arg_piece_color: PieceColor):
        self.piece_color = arg_piece_color


