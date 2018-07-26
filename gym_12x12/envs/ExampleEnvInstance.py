from gym_12x12.envs.gym12x12_env import gym12x12_env, PlayerType as pt
import time as tmr


env = gym12x12_env()

player_one = env.create_player(pt.BOT, dumb_bot_ai=True, argname="bot1")
player_two = env.create_player(pt.BOT, dumb_bot_ai=False, argname="bot2")
env.initiate_game(arg_player1=player_one, arg_player2=player_two, arg_int_boardsize=6)
float_game_speed_in_seconds = 1

for i_episode in range(2):
    obs = env.reset()
    done = None
    i = 0
    while not done:
        action = env.AgentPlayer.get_ai_move(obs)
        obs, reward, done, info = env.step(action)
        env.Game.print_game_board()
        env.render()
        tmr.sleep(float_game_speed_in_seconds)

        if done:
            print("Finished. Episode", i_episode, "score ", "BLUE:", env.Game.PlayerOneScore, " RED:", env.Game.PlayerTwoScore)
            print(env.Game.captured_pieces)
            # tmr.sleep(2)

