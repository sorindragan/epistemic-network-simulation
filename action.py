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

    # bernoulli distributed payoff with p = 1/2 for both states
    def do(self, state) -> int:
        if type(state) != type(State(0)):
            print("The given state was not valid")
        
        rv = bernoulli(p=0.5)
        return rv.rvs(), rv.pmf(1)
    

class ActionB(Action):
    def __init__(self, epsilon) -> None:
        super().__init__()
        self.name = "Action B"
        self.epsilon = epsilon

    # bernoulli distributed payoff with p = 1/2 +- epsilon depending on the state
    def do(self, state) -> int:
        if type(state) != type(State(0)):
            print("The given state was not valid")
        
        if state.id == 1:
            rv = bernoulli(p=(0.5 + self.epsilon))
            return rv.rvs(), rv.pmf(1)
        
        if state.id == 2:
            rv = bernoulli(p=(0.5 - self.epsilon))
            return rv.rvs(), rv.pmf(1)
        
        print("It should not reach this point")
        return 1, 0.5 if rand.uniform(0, 1) > 0.5 else 0, 0.5