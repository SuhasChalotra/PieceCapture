from gym_12x12.envs.env_classes.game import Game
from gym_12x12.envs.env_classes.player import BotPlayer, HumanPlayer, AgentPlayer

p2 = BotPlayer()
p1 = AgentPlayer()

g = Game(p1, p2, 6, 6)

move_row, move_col = p2.get_random_move(g.empty_spots)
g.place_piece(p2, move_row, move_col)
g.print_game_board()
print("Empty Spots", len(g.empty_spots))

print(p2.will_move_endanger_player([3, 4], g.Board))
strat = p2.get_strategies(g.Board)
print(strat)
