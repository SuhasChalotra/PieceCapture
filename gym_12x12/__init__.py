from gym.envs.registration import register

register(
    id='12x12-v0',
    entry_point='gym_12x12.envs:gym12x12_env'
)