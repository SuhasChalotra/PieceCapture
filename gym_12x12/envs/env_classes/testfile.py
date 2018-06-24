from gym_12x12.envs.env_classes.game import Game
from gym_12x12.envs.env_classes.player import Player, AIPlayer, HumanPlayer

p1 = AIPlayer(0)
p2 = AIPlayer(1)
gme = Game(p1, p2)

gme.referee_assess()