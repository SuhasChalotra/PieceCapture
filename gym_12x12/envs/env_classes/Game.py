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
            raise ValueError("Gmaeboard: type must be of type gameboard")

        if isinstance(arg_player1, Player):
            self.Player1 = arg_player1
        else:
            raise ValueError("Player 1: type must be of type Player")

        if isinstance(arg_player2, Player):
            self.Player2 = arg_player2
        else:
            raise ValueError("Player 2: type must be of type Player")

        self.assign_player_piece_color()  # ensure piece colors are different for each player
        return

    def assign_player_piece_color(self):
        # This method will ensure that the players have unique piece colors and should correct
        # the piece color assignment should it be invalid
        # We need to check if the Player1 and Player2 fields of the game are null.
        if self.Player1.piece_color == PieceColor.BLUE and self.Player2.piece_color == PieceColor.BLUE:
            # Players have the same color, so change them
            self.Player1.piece_color = PieceColor.BLUE
            self.Player2.piece_color = PieceColor.RED
            print('Player colors were the same, so we changed them')
        elif self.Player1.piece_color == PieceColor.RED and self.Player2.piece_color == PieceColor.RED:
            # Both players have the same piece color (red), so ensure they are different
            self.Player1.piece_color = PieceColor.BLUE
            self.Player2.piece_color = PieceColor.RED
            print('Player colors were the same, so we changed them')
        else:
            print('Piece colors are fine')

        return

    def place_piece(self, arg_player: Player, xloc, yloc):
        # This will place a player's piece in the matrix
        # We need to make sure it can only place a piece in an empty slot
        pass
