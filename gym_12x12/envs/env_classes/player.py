from abc import ABCMeta, abstractmethod
from gym_12x12.envs.env_classes.PieceColor import PieceColor

# Games need players. But we should only be able to instantiate a HumanPlayer or an AIPlayer
# As Player is an abstract class


class Player (object):
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


