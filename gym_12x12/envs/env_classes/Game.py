from gym_12x12.envs.env_classes.player import Player
from gym_12x12.envs.env_classes.Gameboard import GameBoard, PieceColor


class Game:
    # This starts a new game / session. It should be initialized w/ a Gameboard and two player
    # objects
    def __init__(self, arg_game_board: GameBoard, arg_player1: Player, arg_player2: Player):
        # Must ensure that the correct object type is passed as parameters
        if isinstance(arg_game_board, GameBoard):
            self._GameBoard = arg_game_board
        else:
            raise ValueError("Type must be of type Gameboard")

        if isinstance(arg_player1, Player):
            self.Player1 = arg_player1
        else:
            raise ValueError("Player 1: Type must be of type Player")

        if isinstance(arg_player2, Player):
            self.Player2 = arg_player2
        else:
            raise ValueError("Player 2: Type must be of type Player")

        return

    def assign_player_piece_color(self):
        # This method will ensure that the players have unique piece colors and should correct
        # the piece color assignment should it be invalid
        # We need to check if the Player1 and Player2 fields of the game are null.
        if self.Player1.piece_color == PieceColor.BLUE and self.Player2.piece_color == PieceColor.BLUE:
            # Players have the same color
            print('Player colors were the same, changed')

        return

    def place_piece(self, arg_player: Player, xloc, yloc):
        # This will place a player's piece in the matrix
        # We need to make sure it can only place a piece in an empty slot
        pass