import numpy.random as rand
from scipy.stats import bernoulli

from state import State

class Action:
    def __init__(self) -> None:
        pass

class ActionA(Action):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Action A"

    def do(self, state):
        if type(state) != type(State(0)):
            print("The given state was not valid")
        
        return bernoulli.rvs(p=0.5, size=1)[0]


class ActionB(Action):
    def __init__(self, epsilon) -> None:
        super().__init__()
        self.name = "Action B"
        self.epsilon = epsilon

    def do(self, state) -> int:
        if type(state) != type(State(0)):
            print("The given state was not valid")
        
        if state.id == 1:
            return bernoulli.rvs(p=(0.5 + self.epsilon), size=1)[0]
        
        if state.id == 2:
            return bernoulli.rvs(p=(0.5 - self.epsilon), size=1)[0]
        
        print("It should not reach this point")
        return 1 if rand.uniform(0, 1) > 0.5 else 0
