import gym
from gym import spaces
from multiOneHot import multiOneHotEncoding
import numpy as np
import itertools as it


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

        info : error string for diagnostic purposes only

    """
    metadata = {'render.modes': ['human']}

    def __init__(self, n=3, end_t=15, lambdaMatrix=None,rho=0.5):
        # Initialize the values
        self.n = n  # Number of input/output queues
        self.end_t = end_t  # last time step
        self.statuses = ['ONGOING', 'OVER']  # Status definitions
        if lambdaMatrix is None:  # lambda matrix for arrivals
            self.lambdaMatrix = (np.ones((self.n, self.n))*rho)/(self.n)
        else:
            self.lambdaMatrix = lambdaMatrix

        # Setup the spaces for learners
        self.action_space_actual = multiOneHotEncoding(
            [n, n])  # Binary one hot matrix input space
        self.validActions = self.generateValidActions()  # Generates all possible actions
        # We have length(validActions) discrete possible actions
        self.action_space = spaces.Discrete(len(self.validActions))
        self.observation_space = spaces.Box(
            low=0, high=np.inf, shape=(n, n), dtype=int)  # nxn queue observation space
        self.reset()

    def generateValidActions(self):
        # Generate all possible
        allwords = list(it.product(*([(0, 1)] * (self.n**2))))
        allarrays = map(np.asarray, allwords)  # Convert to array
        allmatrices = [a.reshape(self.n, self.n)
                       for a in allarrays]  # Matrixify
        validActions = [
            x for x in allmatrices if self.action_space_actual.contains(x)]
        return validActions

    def reset(self):
        self.state = np.zeros((self.n, self.n))  # Starting state is all zeros
        self._update_state()  # Initialize a starting state
        self.status = self.statuses[0]  # Starting status is ongoing
        self.t = 0  # time steps

        # return np.array([self._get_state(), 0, self._get_status(), "NONE"])
        return self._get_state()
    def step(self, action):

        # Check if action is valid:
        # Make sure no queue goes below zero and action is valid
        if self.status == self.statuses[1]:
            raise RuntimeError("Game is done")
        # if (not self.action_space.contains(action)) or np.any((self.state - action) < 0):
        #     reward = -100
        #     self.status = self.statuses[0]
        #     done = self._get_status()
        #     ob = self._get_state()
        #     info = "INVALID ACTION"
        #     return ob, reward, done, info
        # else:
        self._take_action(action)
        done = self._get_status()
        reward = self._get_reward()
        self._update_state()
        ob = self._get_state()
        info = "ACTION TAKEN"

        return np.array([ob, reward, done, {}])

    def _render(self, mode='human', close=False):
        return

    def _take_action(self, action):
        # Map action number to actual action
        curAction = self.validActions[action]
        self.state = self.state - curAction  # Subtract from the queues
        self.state[self.state < 0] = 0
        self.t = self.t + 1  # increase the time step
        if self.t >= self.end_t:  # Check if we are now done
            self.status = self.statuses[1]

    def _update_state(self): #IS THIS VALID
        arrivals = np.random.binomial(
            1, self.lambdaMatrix).reshape((self.n, self.n))
        self.state += arrivals
        # while np.all(self.state == 0):  # Make sure there is atleast 1 element in the queue
        #     print("here")
        #     arrivals = np.random.binomial(
        #         1, self.lambdaMatrix).reshape((self.n, self.n))
        #     self.state += arrivals

    def _get_reward(self):
        """ Reward is given for current state """
        return -np.sum(self.state)

    def _get_state(self):
        return self.state

    def _get_status(self):
        """ Reward is given for current state """
        if self.status == self.statuses[0]:  # ONGOING
            return False
        elif self.status == self.statuses[1]:  # DONE
            return True
