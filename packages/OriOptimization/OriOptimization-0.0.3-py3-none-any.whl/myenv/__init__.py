from gym.envs.registration import register

register(
    id="OriOptimization-v0",
    entry_point="myenv.envs.ori_optimize:OriOptimizeEnv",
    max_episode_steps=100,
)