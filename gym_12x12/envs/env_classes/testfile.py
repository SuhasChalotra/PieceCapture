from gym_12x12.envs.env_classes.game import Game
from gym_12x12.envs.env_classes.player import Player, AIPlayer, HumanPlayer

p1 = AIPlayer()
p2 = AIPlayer()
gme = Game(p1, p2)

gme.place_piece(p2, 11, 5)

gme.place_piece(p1, 11, 4)
gme.place_piece(p1, 11, 6)
gme.place_piece(p1, 10, 5)

gme.place_piece(p1, 5, 5)

gme.place_piece(p2, 4, 5)
gme.place_piece(p2, 6, 5)
gme.place_piece(p2, 5, 4)
gme.place_piece(p2, 5, 6)

gme.place_piece(p2, 0, 5)

gme.place_piece(p1, 0, 4)
gme.place_piece(p1, 0, 6)
gme.place_piece(p1, 1, 5)

print(gme.Board.Grid)
gme.sweep_board()
