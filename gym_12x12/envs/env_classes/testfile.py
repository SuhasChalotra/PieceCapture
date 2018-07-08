from gym_12x12.envs.env_classes.game import Game
from gym_12x12.envs.env_classes.player import BotPlayer, HumanPlayer

p2 = BotPlayer()
p1 = HumanPlayer()

g = Game(p1, p2, 6, 6)

strat = p2.get_strategies(g.Board)
print(strat)







