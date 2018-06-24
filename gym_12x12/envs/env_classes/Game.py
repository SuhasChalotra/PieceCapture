from gym_12x12.envs.env_classes.player import Player, AIPlayer, HumanPlayer
from gym_12x12.envs.env_classes.Gameboard import GameBoard


class Game:
    # This starts a new game / session. It should be initialized w/ a Gameboard and two player
    # objects

    GAME_MOVE_INVALID = -1
    GAME_MOVE_VALID = 0
    EMPTY = 0
    RED = 1
    BLUE = 2

    def __init__(self, player_1, player_2, arg_size_x=12, arg_size_y=12):
        # Must ensure that the correct object type is passed as parameters

        if isinstance(player_1, Player):
            self.Player1 = player_1
        else:
            raise ValueError("Player 1: type must be of type Player")

        if isinstance(player_2, Player):
            self.Player2 = player_2
        else:
            raise ValueError("Player 2: type must be of type Player")

        self.__assign_player_piece_color()  # ensure piece colors are different for each player
        #  Create a new game board
        self._GameBoard = GameBoard(size_x=arg_size_x, size_y=arg_size_y)

        # These fields keep track of players' scores
        self.P1Score = 0
        self.P2Score = 0

    def __assign_player_piece_color(self):
        # This private method will ensure that the players have unique piece colors and should correct
        # the piece color assignment should it be invalid.
        # We need to check if the Player1 and Player2 fields of the game are null or of the incorrect type
        if self.Player1.piece_color == Game.BLUE and self.Player2.piece_color == Game.BLUE:
            # Players have the same color, so change them
            self.Player1.piece_color = Game.BLUE
            self.Player2.piece_color = Game.RED
            print('Player colors were the same, so we changed them')
        elif self.Player1.piece_color == Game.RED and self.Player2.piece_color == Game.RED:
            # Both players have the same piece color (red), so ensure they are different
            self.Player1.piece_color = Game.BLUE
            self.Player2.piece_color = Game.RED
            print('Player colors were the same, so we changed them')
        elif self.Player1.piece_color == Game.EMPTY or self.Player2.piece_color == Game.EMPTY:
            # A player's piece color has been assigned as empty, which is not allowed
            self.Player1.piece_color = Game.BLUE
            self.Player2.piece_color = Game.RED
            print('One of the piece colors were assigned as empty; corrected.')
        return

    def place_piece(self, arg_player: Player, xloc, yloc):
        # This will place a player's piece in the game_board matrix
        # We need to make sure it can only place a piece in an empty slot

        # x and y need to be within range and be valid integers
        if not isinstance(xloc, int):
            raise ValueError("x location must be an integer")
            return Game.GAME_MOVE_INVALID

        if not isinstance(yloc, int):
            raise ValueError("y location must be an integer")
            return Game.GAME_MOVE_INVALID

        if xloc < 0 or xloc > self._GameBoard.XSize:
            print("x is out of range. x=", xloc)
            return Game.GAME_MOVE_INVALID

        if yloc < 0 or yloc > self._GameBoard.YSize:
            print("y is out of range. y=", yloc)
            return Game.GAME_MOVE_INVALID

        if self._GameBoard.Grid[xloc, yloc] == Game.EMPTY:  # Empty slot to play
            self._GameBoard.Grid[xloc, yloc] = arg_player.piece_color
            return Game.GAME_MOVE_VALID
        else:
            """ Nothing should really happen, and the attempting player should be allowed to play another move.
            We'll return a value to indicate to the calling code
            that the game move is invalid, and that the player should try again.
            This will only ever happen with human players. The AI will never attempt to play a piece
            in a slot that is occupied, as it will check before doing so. It also should never
            play an invalid move (ex. index out of rage)
            """
            print("Invalid move. Try again.")
            return Game.GAME_MOVE_INVALID

    def print_game_board(self):
        # This prints the game board contents
        print(self._GameBoard.Grid)

    def referee_assess(self):
        """
        This scans the game board and keeps track of the scores
        :return:
        """
        i = 0
        # As a test, let's iterate through the Game board
        for row in self._GameBoard.Grid:
                print(i)
                i += 1
                # print(row_index, col_index)
                # print(self._GameBoard.Grid[row_index, col_index])


Human = HumanPlayer(Game.BLUE)
AI = AIPlayer(Game.RED)
game = Game(Human, AI)

# game.place_piece(AI, 0, 0)
# game.place_piece(Human, 0, 1)
# Test
print(game._GameBoard)
