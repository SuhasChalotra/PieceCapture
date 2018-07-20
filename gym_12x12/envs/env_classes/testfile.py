from gym_12x12.envs.env_classes.game import Game
from gym_12x12.envs.env_classes.player import BotPlayer, HumanPlayer, AgentPlayer

p2 = BotPlayer()
p1 = AgentPlayer()

g = Game(p1, p2, 6, 6)

move_row, move_col = p2.get_random_move(g.empty_spots)
g.place_piece(p2, 0, 1)
g.place_piece(p1, 0, 2)
g.place_piece(p2, 0, 3)
g.print_game_board()

strat = p2.get_ai_move(g.Board)
print(strat)
