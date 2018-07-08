from gym_12x12.envs.env_classes.game import Game
from gym_12x12.envs.env_classes.player import BotPlayer, HumanPlayer

p2 = BotPlayer()
p1 = HumanPlayer()

g = Game(p1, p2, 6, 6)
g.place_piece(p1, 3, 3)
g.place_piece(p1, 3, 5)
g.place_piece(p1, 2, 4)
# g.place_piece(p1, 4, 4)
g.print_game_board()

print(p2.will_move_endanger_player([3, 4], g.Board))
strat = p2.get_strategies(g.Board)
print(strat)







