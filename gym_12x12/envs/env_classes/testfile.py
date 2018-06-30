from gym_12x12.envs.env_classes.game import Game
from gym_12x12.envs.env_classes.player import AIPlayer, HumanPlayer
import time

start_time = time.time()
p1 = AIPlayer()
p2 = AIPlayer()
gme = Game(p1, p2)

p1.get_strategies(gme)

gme.place_piece(p2, 0, 0)
gme.place_piece(p1, 0, 1)
gme.place_piece(p2, 1, 0)

print(gme.Board.Grid)

print("My program took", time.time() - start_time, "to run")
