from gym_12x12.envs.env_classes.player import Player, AIPlayer, HumanPlayer
from gym_12x12.envs.env_classes.Gameboard import GameBoard, PieceColor


class Game:
    # This starts a new game / session. It should be initialized w/ a Gameboard and two player
    # objects

    GAME_MOVE_INVALID = "invalid"

    def __init__(self, arg_game_board: GameBoard, arg_player1: Player, arg_player2: Player):
        # Must ensure that the correct object type is passed as parameters
        if isinstance(arg_game_board, GameBoard):
            self._GameBoard = arg_game_board
        else:
            raise ValueError("Game board: type must be of type gameboard")

        if isinstance(arg_player1, Player):
            self.Player1 = arg_player1
        else:
            raise ValueError("Player 1: type must be of type Player")

        if isinstance(arg_player2, Player):
            self.Player2 = arg_player2
        else:
            raise ValueError("Player 2: type must be of type Player")

        self.__assign_player_piece_color()  # ensure piece colors are different for each player
        return

    def __assign_player_piece_color(self):
        # This private method will ensure that the players have unique piece colors and should correct
        # the piece color assignment should it be invalid.
        # We need to check if the Player1 and Player2 fields of the game are null or of the incorrect type
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
        elif self.Player1.piece_color == PieceColor.EMPTY or self.Player2.piece_color == PieceColor.EMPTY:
            # A player's piece color has been assigned as empty, which is not allowed
            self.Player1.piece_color = PieceColor.BLUE
            self.Player2.piece_color = PieceColor.RED
            print('One of the piece colors were assigned as empty; corrected.')
        return

    def place_piece(self, arg_player: Player, xloc, yloc):
        # This will place a player's piece in the game_board matrix
        # We need to make sure it can only place a piece in an empty slot

        piece_to_play = arg_player.piece_color

        if self._GameBoard.Grid[xloc, yloc] == PieceColor.EMPTY:  # Empty slot to play
            self._GameBoard.Grid[xloc, yloc] = piece_to_play
        else:
            """ Nothing should really happen, and the attempting player should be allowed to play another move.
            We'll return a value to indicate to the calling code
            that the game move is invalid, and that the player should try again.
            This will only ever happen with human players. The AI will never attempt to play a piece
            in a slot that is occupied, as it will check before doing so.
            """
            return Game.GAME_MOVE_INVALID

        pass

    def print_game_board(self):
        # This prints the game board contents
        print(self._GameBoard.Grid)


# Testing initialization of objects required
board = GameBoard()
AI = AIPlayer(PieceColor.BLUE)
PL = HumanPlayer(PieceColor.RED)

# Create a new game
g = Game(board, PL, AI)
g.print_game_board()  # Test print gameboard


