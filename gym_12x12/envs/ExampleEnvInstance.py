from gym_12x12.envs.gym12x12_env import gym12x12_env, PlayerType as pt
import time as tmr


env = gym12x12_env()

player_one = env.create_player(pt.HUMAN, smart_ai=False, argname="human")
player_two = env.create_player(pt.BOT, smart_ai=True, argname="bot2")
env.initiate_game(arg_player1=player_one, arg_player2=player_two, arg_int_boardsize=6, arg_game_type=env.GAME_TYPE_BOT_V_HUMAN, arg_render=True)
float_game_speed_in_seconds = 0

# These are test variables for stats
blue_data_score = []
red_data_score = []
tie_data = []
##########################################

for i_episode in range(1):
    obs = env.reset()
    done = None
    i = 0

    while not done:
        action = env.from_int_to_tuple(env.action_space.sample())
        obs, reward, done, info = env.step(action)
        # env.render()
        tmr.sleep(float_game_speed_in_seconds)
        if done:
            # print("Finished. Episode", i_episode, "score ", "BLUE:", env.Game.PlayerOneScore, " RED:", env.Game.PlayerTwoScore)
            blue_data_score.append(env.Game.PlayerOneScore)
            red_data_score.append(env.Game.PlayerTwoScore)
            if env.Game.PlayerOneScore == env.Game.PlayerTwoScore:
                tie_data.append(tuple([i_episode, env.Game.PlayerOneScore, env.Game.PlayerTwoScore]))


def get_stats_average(blue_data, red_data):
    """
    Returns average score for each color and total episodes played
    :param blue_data: a list
    :param red_data:  a list
    :return: (Total, episodes blue score average, red score average)
    """
    final_blue = sum(blue_data) / len(blue_data)
    final_red = sum(red_data) / len(red_data)
    total_eps = len(blue_data)
    return total_eps, final_blue, final_red


def get_stats_high_score(blue_data, red_data):
    final_highest_blue = max(blue_data)
    final_highest_red = max(red_data)

    return final_highest_blue, final_highest_red

def get_wins_ties():
    blue_wins = 0
    red_wins = 0
    total_ties = len(tie_data)

    # Get wins
    for index in range(len(blue_data_score)):
        if not blue_data_score == red_data_score:
            # ensure we are not counting ties
            if blue_data_score > red_data_score:
                blue_wins += 1
            else:
                red_wins += 1

    # Let's return the ties as a percentage of the total eps
    pecentage_ties = total_ties / len(blue_data_score)
    print("Total episodes: ", len(blue_data_score))

    if blue_wins > red_wins:
        print("Blue win count is", blue_wins - len(tie_data), " red win count is:", red_wins, " tie percentage: ", pecentage_ties * 100, "%")
        print("Blue wins", (blue_wins - total_ties) / len(blue_data_score) * 100, "% of eps. Red Wins", red_wins / len(blue_data_score) * 100, "% of eps.")
    elif blue_wins < red_wins:
        print("Blue win count is", blue_wins, " red win count is:", red_wins - len(tie_data), " tie percentage: ", pecentage_ties * 100, "%")
        print("Blue wins", blue_wins / len(blue_data_score) * 100, "% of eps. Red Wins", (red_wins - total_ties) / len(blue_data_score) * 100, "% of eps.")

    max_tie = 0
    for index in range(len(tie_data) - 1):
        if tie_data[index][1] > max_tie:
            max_tie = tie_data[index][1]

    print("Highest tie is:", max_tie)


t_eps, blue, red = get_stats_average(blue_data_score, red_data_score)
blue, red = get_stats_high_score(blue_data_score, red_data_score)
print("Highest score:", "BLUE:", blue, "RED:", red)
print("Number of ties:", len(tie_data))
print(tie_data)
get_wins_ties()
