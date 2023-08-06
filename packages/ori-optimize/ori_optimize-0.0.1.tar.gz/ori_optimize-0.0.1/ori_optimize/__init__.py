from gym.envs.registration import register

register(
    id="ori_optimize-v0",
    entry_point="ori_optimize.envs.ori_optimize:OriOptimizeEnv",
    max_episode_steps=100,
)