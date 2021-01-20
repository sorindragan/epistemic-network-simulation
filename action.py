import numpy.random as rand

class Action:
    def __init__(self) -> None:
        pass

class ActionA(Action):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Action A"

    def do(self):
        return 1 if rand.uniform(0, 1) > 0.5 else 0

class ActionB(Action):
    def __init__(self, epsilon) -> None:
        super().__init__()
        self.name = "Action B"
        self.epsilon = epsilon

    def do(self):
        return 1 if rand.uniform(0, 1) + self.epsilon > 0.5 else 0
