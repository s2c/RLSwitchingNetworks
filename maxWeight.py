import numpy as np


class maxWeight:
    def __init__(self, env):
        self.env = env
        self.curAction = np.zeros((env.n, env.n))

    # State of the queue after action or before action??? # Actually doesn't matter right? 
    def calcWeight(self, action,alpha=1): # Check the alpha
        nz = np.nonzero(action)
        # Get the queue length in for each assosciated action
        weightIndividual = [self.env.state[i][nz[1][i]] for i in range(0, self.env.n)]
        return sum([i**alpha for i in weightIndividual])

    def act(self,alpha=1):
        curAction = None
        curWeight = -1
        for i, action in enumerate(self.env.validActions):
            weight = self.calcWeight(action,alpha)
            if weight > curWeight:
                curAction = i
                curWeight = weight
            # if weight == curWeight # Fix this again
        return curAction