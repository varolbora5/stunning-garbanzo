import typing
from dataclasses import dataclass
import random
from typing_extensions import List

@dataclass
class Move:
    direction: List[int]

# @dataclass
# class Split:
#     direction: List[int]
# they do not split by decision

Decision = Move |  None

class Vegetob(): # DarkGreen
    def __init__(self, density) -> None:
        self.density = density
        self.color = 2

    def get_density(self):
        return self.density

    def grow(self):
        if self.density < 100:
            self.density += random.randint(1,10)
        return self

class Carviz(): # Red
    def __init__(self, energy = 0, social_attitude=0) -> None:
        self.energy = energy
        self.lifetime = 100
        self.age = 80
        self.social = social_attitude
        self.was_attacked = False
        self.color = 1

    def decide(self, map) -> Decision:
        self.age += 1
        return Move([random.randint(-1,1), random.randint(-1,1)])

class Erbast: # Yellow
    def __init__(self, energy=0, social_attitude=0) -> None:
        self.energy = energy
        self.lifetime = 100
        self.age = 80
        self.social = social_attitude
        self.was_attacked = False
        self.color = 3

    def decide(self, map) -> Decision:
        self.age += 1
        return Move([random.randint(-1,1), random.randint(-1,1)])
