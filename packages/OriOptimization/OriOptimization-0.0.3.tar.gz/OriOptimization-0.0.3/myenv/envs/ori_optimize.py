import gym
import torch
from gym import spaces
import numpy as np
import Support
import math

env = Support.Calculation()


class OriOptimizeEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode=None, initial_ori=np.array([1, 0, 0])):
        self.env = env
        # self.observation_space = ?

        # rotate model around TWO axis of the XYZ is enough
        self.action_space = spaces.Discrete(2)

        # 模型初始方向
        self.initial_ori = initial_ori
        self._agent_orientation = self.initial_ori

        # 这里说明每次旋转模型，模型绕某个轴旋转 pi/36 = 5°
        self.cos = math.cos(math.pi / 36)
        self.sin = math.sin(math.pi / 36)

        # 下面的是旋转矩阵 0: 绕"x" 1: 绕"y"
        self._action_to_direction = {
            0: np.array([[1, 0, 0],
                         [0, self.cos, -self.sin],
                         [0, self.sin, self.cos]]),
            1: np.array([[self.cos, 0, self.sin],
                         [0, 1, 0],
                         [-self.sin, 0, self.cos]])
        }

        self._target_orientation = np.array([0, 0, 1])

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        # 目前不知用处，设置为None
        self.window = None
        self.clock = None

    def model_object(self, file_path):
        # 这个位置传入文件地址，设定模型
        return self.env.getFilePath(file_path)

    def _get_obs(self):
        self.picture = torch.tensor((3, 227, 227))
        # 这里会获得一个模型当前角度
        # 这里会修改picture,传递当前的模型旋转的图片信息
        return {"agent": self.picture}

    def _get_info(self):
        # 暂时没什么info需要返回
        return {"orientation": self._agent_orientation}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._agent_orientation = self.initial_ori

        # 重置环境其实就是将模型的角度摆正，摆回原来的位置
        self.env.getInitialOri([1, 0, 0])

        observation = self._get_obs()
        info = self._get_info()

        # if self.render_mode == "human":
        #     self._render_frame()

        return observation, info

    def step(self, action):
        angle = self._action_to_direction[action]
        self._agent_orientation = self._agent_orientation.dot(angle)

        self.env.getOri(self._agent_orientation)
        support_area = self.env.runCompute()
        # 是否结束
        terminated = np.array_equal(self._agent_orientation, self._target_orientation)

        # 如果结束获得奖励，未结束的时候获得的奖励不能为0，应该为负，避免模型停在原地不动
        reward = -0.1 if terminated else 0

        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, terminated, False, info

    # def render(self):
    #     if self.render_mode == "rgb_array":
    #         return self._render_frame()