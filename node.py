from state import State
import numpy as np
import numpy.random as rand

from action import ActionA, ActionB

VERBOSE = False

class AgentNode:
    def __init__(self, id):
        self.id = id

class ScientistNode(AgentNode):
    def __init__(self, id):
        super().__init__(id)
        self.belief = rand.uniform(0, 1)
        self.action_a = ActionA()
        self.action_b = ActionB(0.05)
        self.outcome = None
        self.pmf = None
        self.neighbours = []
    
    def __repr__(self) -> str:
        return f"<ID: {self.id} \nBelief: {self.belief} \nNeighbours: {[n.id for n in self.neighbours]}>"
    
    def set_belief(self, belief):
        self.belief = belief

    def add_neighbour(self, neigbour) -> None:
        self.neighbours.append(neigbour)
    
    def define_neighbours(self, neighbours_list) -> None:
        self.neighbours = neighbours_list
    
    def pick_action(self):
        if self.belief < 0.5:
            return self.action_a
        
        if self.belief >= 0.5:
            return self.action_b
        
        print("This point should not be reached")

    def act(self) -> None:
        payoff = None
        p = None
        if self.belief < 0.5:
            payoff, p = self.action_a.do(State(1))
        
        if self.belief >= 0.5:
            payoff, p = self.action_b.do(State(1))
        
        if payoff is None:
            print("This point should not have been reached - None Payoff")

        self.outcome, self.pmf = payoff, p
    
    def update_belief(self):
        prior = self.belief
        nomerator = np.prod([n.pmf for n in self.neighbours]) * prior
        denominator = sum([np.prod([n.pick_action().do(state)[1] 
                                    for n in self.neighbours]) * (prior if state.id == 1 else (1 - prior))
                            for state in [State(1), State(2)]])
        self.belief = nomerator / denominator
        
        if VERBOSE:
            print(f"{self.id} : {self.belief}")
        
    
