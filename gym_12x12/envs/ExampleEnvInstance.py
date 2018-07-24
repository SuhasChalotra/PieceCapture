from gym_12x12.envs.gym12x12_env import gym12x12_env, PlayerType as pt
import time as tmr


env = gym12x12_env()

player_one = env.create_player(pt.BOT, dumb_bot_ai=False, argname="bot1")
player_two = env.create_player(pt.BOT, dumb_bot_ai=False, argname="bot2")
env.initiate_game(arg_player1=player_one, arg_player2=player_two, arg_int_boardsize=6)
float_game_speed_in_seconds = 1.5

for i_episode in range(1):
    obs = env.reset()

    while True:
        # print("Move by ", env.CurrentPlayer.name)
        action = env.CurrentPlayer.get_ai_move(obs)
        observation, reward, done, info = env.step(action)
        env.alternate_player()
        env.render()
        tmr.sleep(float_game_speed_in_seconds)

        if done:
            print("Finished. Episode", i_episode, "score ", "BLUE:", env.Game.PlayerOneScore, " RED:", env.Game.PlayerTwoScore)
            break





