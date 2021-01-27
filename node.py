from state import State
import numpy as np
import numpy.random as rand

from action import ActionA, ActionB

VERBOSE = False
EPSILON = 0.05


class AgentNode:
    def __init__(self, id):
        self.id = id


class ScientistNode(AgentNode):
    def __init__(self, id):
        super().__init__(id)
        self.type = "Scientist"
        self.belief = rand.uniform(0, 1)
        self.action_a = ActionA()
        self.action_b = ActionB(EPSILON)
        self.outcome = None
        self.pmf = None
        self.neighbours = []
    
    def __repr__(self) -> str:
        return f"<Type: {self.type} \nID: {self.id}\nBelief: {self.belief} \nNeighbours: {[n.id for n in self.neighbours]}>\n"
    
    def set_belief(self, belief):
        self.belief = belief

    def add_neighbour(self, neigbour) -> None:
        if neigbour not in self.neighbours:
            self.neighbours.append(neigbour)
    
    def remove_neighbour(self, neighbour) -> None:
        if neighbour in self.neighbours:
            self.neighbours.remove(neighbour)
    
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
        

class PolicymakerNode(AgentNode):
    def __init__(self, id):
        super().__init__(id)
        self.type = "Policymaker"
        self.belief = rand.uniform(0, 0.5)
        self.action_a = ActionA()
        self.action_b = ActionB(EPSILON)
        self.neighbours = []

    def __repr__(self) -> str:
        return f"<Type: {self.type} \nID: {self.id}\nBelief: {self.belief} \nNeighbours: {[n.id for n in self.neighbours]}>\n"

    def set_belief(self, belief):
        self.belief = belief

    def add_neighbour(self, neigbour) -> None:
        if neigbour not in self.neighbours:
            self.neighbours.append(neigbour)

    def remove_neighbour(self, neighbour) -> None:
        if neighbour in self.neighbours:
            self.neighbours.remove(neighbour)

    def define_neighbours(self, neighbours_list) -> None:
        self.neighbours = neighbours_list

    # Policymakers just update the belief; they do not act
    def update_belief(self):
        prior = self.belief
        nomerator = np.prod([n.pmf for n in self.neighbours]) * prior
        denominator = sum([np.prod([n.pick_action().do(state)[1]
                                    for n in self.neighbours]) * (prior if state.id == 1 else (1 - prior))
                           for state in [State(1), State(2)]])
        self.belief = nomerator / denominator

        if VERBOSE:
            print(f"{self.id} : {self.belief}")


class JournalistNode(AgentNode):
    def __init__(self, id):
        super().__init__(id)
        self.type = "Journalist"
        self.belief = rand.uniform(0, 1)
        self.action_a = ActionA()
        self.action_b = ActionB(EPSILON)
        self.outcome = None
        self.pmf = None
        self.neighbours = []
    
    def __repr__(self) -> str:
        return f"<Type: {self.type} \nID: {self.id}\nBelief: {self.belief} \nNeighbours: {[n.id for n in self.neighbours]}>\n"

    def set_belief(self, belief):
        self.belief = belief

    def add_neighbour(self, neigbour) -> None:
        if neigbour not in self.neighbours:
            self.neighbours.append(neigbour)
    
    def remove_neighbour(self, neighbour) -> None:
        if neighbour in self.neighbours:
            self.neighbours.remove(neighbour)
    
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
    
    # Journalists update their beliefs in a special random way
    def update_belief(self):
        neighbour_beliefs = []
        neighbour_beliefs_le = [n.belief for n in self.neighbours
                                if n.belief < 0.5
                                ]
        neighbour_beliefs_ge = [n.belief for n in self.neighbours
                                if n.belief >= 0.5
                                ]

        if len(neighbour_beliefs_le) > 0 and len(neighbour_beliefs_ge) > 0:
            if rand.uniform(0, 1) < 0.5:
                neighbour_beliefs = neighbour_beliefs_le
            else:
                neighbour_beliefs = neighbour_beliefs_ge
        elif len(neighbour_beliefs_le) > 0:
            neighbour_beliefs = neighbour_beliefs_le
        elif len(neighbour_beliefs_ge) > 0:
            neighbour_beliefs = neighbour_beliefs_ge
     
        if len(neighbour_beliefs) == 0:
            print("Theoretically, this point shoudl not be reached")
            neighbour_beliefs = [rand.uniform(0, 1)]
        
        self.belief = sum(neighbour_beliefs) / len(neighbour_beliefs)
 
        if VERBOSE:
            print(f"{self.id} : {self.belief}")
