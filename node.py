import numpy as np
import numpy.random as rand

from action import ActionA, ActionB


class Node:
    def __init__(self, id):
        self.id = id

class ScientistNode(Node):
    def __init__(self, id):
        super().__init__(id)
        self.credence = rand.uniform(0, 1)
    
    def __repr__(self) -> str:
        return f"<ID: {self.id} - Credence: {self.credence}>"
    
    def test_theory(self):
        pass
    