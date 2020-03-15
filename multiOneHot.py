import gym
import numpy as np
import collections


class multiOneHotEncoding(gym.Space):  # create one hot vector
    """
    {0,...,1,...,0}

    Example usage:
    self.observation_space = multiOneHotEncoding(shape=(4,4))
    """

    def __init__(self, shape=None):
        assert isinstance(shape, collections.Sequence)  # also nxn always
        gym.Space.__init__(self, (), np.int64)
        self.shape = shape

    def sample(self):
        one_hot_vector = np.zeros(self.shape)  # initialize a 0 vector
        num_1s = np.random.randint(low=0, high=self.shape[0] + 1)
        possible = np.arange(0, num_1s, 1)
        if len(possible) < self.shape[0]:
            numMissing = self.shape[0] - len(possible)
            inserts = -np.ones(numMissing)
            possible = np.append(inserts, possible).astype(int)
        np.random.shuffle(possible)
        for i, curVector in enumerate(one_hot_vector):
            if possible[i] >= 0:
                curVector[possible[i]] = 1
        return one_hot_vector

    def contains(self, x):
        if isinstance(x, (collections.Sequence, np.ndarray)):
            colSums = np.sum(x, axis=0)
            rowSums = np.sum(x, axis=1)
            return (np.all(colSums <= 1) and np.all(rowSums <= 1)) and np.all(x >= 0)
        else:
            return False

    def __repr__(self):
        return "multiOneHotEncoding" + str(self.shape)

    def __eq__(self, other):  # overrage equality
        return self.shape == other.shape
