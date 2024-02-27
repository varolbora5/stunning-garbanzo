import typing
from dataclasses import dataclass
import random
from typing_extensions import List

@dataclass
class Move:
    direction: List[int]

@dataclass
class Attack:
    direction: List[int]

@dataclass
class Graze:
    direction = [0,0]

# @dataclass
# class Split:
#     direction: List[int]
# they do not split by decision

Decision = Move | Graze | Attack | None

class Vegetob(): # DarkGreen
    def __init__(self, density) -> None:
        self.density = density
        self.color = 2

    def get_density(self):
        return self.density

    def set_density(self, x, add=False):
        if add == False:
            self.density = x
        else:
            self.density += x

    def grow(self):
        if self.density < 100:
            self.density += random.randint(1,10)
        return self

class Carviz(): # Red
    def __init__(self, energy=10, social_attitude=0) -> None:
        self.energy = energy
        self.lifetime = 100
        self.age = 80
        self.social_attitude = social_attitude
        self.color = 1

    def set_energy(self, x, add=False):
        if add == False:
            self.energy = x
        else:
            self.energy += x

    def decide(self, map, hunt=False) -> Decision:
        self.age += 1
        return Move([random.randint(-1,1), random.randint(-1,1)])

class Erbast: # Yellow
    def __init__(self, energy=10, social_attitude=0) -> None:
        self.energy = energy
        self.lifetime = 100
        self.age = 80
        self.social_attitude = social_attitude
        self.was_attacked = False
        self.color = 3
        self.grazed = False

    def set_energy(self, x, add=False):
        if add == False:
            self.energy = x
        else:
            self.energy += x

    def decide(self, map) -> Decision:
        self.age += 1
        return Move([random.randint(-1,1), random.randint(-1,1)])
