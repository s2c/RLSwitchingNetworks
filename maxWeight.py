import numpy as np


class maxWeight:
    def __init__(self, env):
        self.env = env
        self.curAction = np.zeros((env.n, env.n))

    # State of the queue after action or before action??? # Actually doesn't matter right?
    def calcWeight(self, action):
        nz = np.nonzero(action)
        # Get the queue length in for each assosciated action
        weightIndividual = [self.env.state[i][nz[1][i]] for i in range(0, 3)]
        return sum(weightIndividual)

    def act(self):
        curAction = None
        curWeight = -1
        for i, action in enumerate(self.env.validActions):
            weight = self.calcWeight(action)
            if weight > curWeight:
                curAction = i
                curWeight = weight
        return curAction