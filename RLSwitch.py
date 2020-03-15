import gym
from gym import spaces
from oneHot import OneHotEncoding
import numpy as np


class RLSwitchEnv(gym.Env):
    """

    Parameters
    ----------
    lambda_i_j =  n x n arrival/matching matrix, input i -> output

    Action :
    ---------
    [n length binary vector] =  Each entry corresponds to which output the input queue is subtracting from
    -1 = Don't send anything from that queue to the output

    Returns
    -------
    ob, reward, episode_over, info : tuple
        ob (object) :
            Q_n : n x n matrix that corresponds to the input and output queues
        reward (float) :
            -sum(Q_n) : negative of sum of all elements in Q_n
        episode_over (bool) :
            - number of timesteps

        info (dict) :
             diagnostic information useful for debugging. It can sometimes
             be useful for learning (for example, it might contain the raw
             probabilities behind the environment's last state change).
             However, official evaluations of your agent are not allowed to
             use this for learning.
    """
    metadata = {'render.modes': ['human']}

    def __init__(self, end_t=15, n=3, lambdaMatrix=None):

        self.n = 3
        self.end_t = 16
        self.statuses = ['ONGOING', 'OVER']
        if lambdaMatrix is None:
            self.lambdaMatrix = [0.5, 0.5, 0.5,
                                 0.5, 0.5, 0.5,
                                 0.5, 0.5, 0.5]
        else:
            self.lambdaMatrix = lambdaMatrix
        self.reset()

    def _reset(self):
        actionTuple = [OneHotEncoding(self.n)] * self.n
        self.action_space = spaces.Tuple(actionTuple)  # n
        self.state = np.zeros((self.n, self.n))
        self.status = self.statuses[0]
        self.Totalreward = 0

    def _step(self, action):

        # Check if action is valid:
        if np.any(state-action) < 0:
            reward = -100

        self._take_action(action)
        self.status = self._get_status()
        reward = self._get_reward()
        ob = self.env.getState()

        return ob, reward, self.status

    def _render(self, mode='human', close=False):
        pass

    def _take_action(self, action):
        # If action is invalid:

                # If action is valid

    def _get_reward(self):
        """ Reward is given for current state """
        return -np.sum(self.state)

    def _get_status(self):
        """ Reward is given for current state """
        if self.status == self.statuses[0]:
            return 0
        elif self.status == self.statuses[1]:
            return 1

