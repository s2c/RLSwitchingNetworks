import numpy as np


class maxWeight:
    def __init__(self, env):
        self.env = env
        self.curAction = np.zeros((env.n, env.n))

    # State of the queue after action or before action??? # Actually doesn't matter right?
    def calcWeight(self, action):
        nz = np.nonzero(action)
        weightIndividual = [self.env.state[i][nz[1][i]] for i in range(0, 3)] # Get the queue length in for each assosciated action 
        return sum(weightIndividual)

    def act(self, state):
        curAction = None
        curWeight = 0
        for action in env.validActions:
            weight = calcWeight(action)
            if weight > curWeight:
                curAction = action
                curWeight = weight
        return curAction