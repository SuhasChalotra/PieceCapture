from twoPlayerTester import PieceCaptureTwoStep
import time as tmr
game = PieceCaptureTwoStep()
game.get_action_space()
done = False

a = tmr.time()
p1_win = 0
for x in range(100):

    game.game.reset()
    p1_score, p2_score = 0, 0
    done = False
    while not done:
        move = game.get_random_move()
        _, reward, done, _ = game.player_one_move(move[0], move[1])
        p1_score += reward[0]
        p2_score += reward[1]

        move = game.get_random_move()
        _, reward, done, _ = game.player_two_move(move[0], move[1])
        p1_score += reward[0]
        p2_score += reward[1]

# if done:
#         print(p1_score, p2_score,x, end = '\r')

#         #game.print()

b = tmr.time()

print(b - a)