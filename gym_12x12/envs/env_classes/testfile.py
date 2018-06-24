from gym_12x12.envs.env_classes.game import Game
from gym_12x12.envs.env_classes.player import Player, AIPlayer, HumanPlayer

p1 = AIPlayer()
p2 = AIPlayer()
gme = Game(p1, p2)

gme.place_piece(p1, 11, 11)

gme.place_piece(p2, 11, 10)
gme.place_piece(p2, 10, 11)

print(gme.Board.Grid)
gme.sweep_board()
