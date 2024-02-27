import typing
from dataclasses import dataclass
import numpy as np
import random
from typing_extensions import List
import itertools
from consts import AGING

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
    def __init__(self, energy=100, social_attitude=0.5) -> None:
        self.energy = energy
        self.max_energy = 100
        self.age = 0
        self.social_attitude = social_attitude
        self.color = 1

    def set_energy(self, x, add=False):
        if add == False:
            self.energy = x
        else:
            self.energy += x
        if self.energy > self.max_energy:
            self.energy = self.max_energy

    def _age(self):
        self.age += 1
        if self.age % 10 == 0:
            self.max_energy -= AGING

    def decide(self, map, hunt=False) -> Decision:
        self._age()
        if hunt == False:
            matrix = [[random.uniform(0.20, 0.40) for _ in range(5)] for _ in range(5)]
            for x in range(map.shape[0]):
                for y in range(map.shape[1]):
                    try:
                        entity = map[x][y].entity[0]
                    except IndexError:
                        entity = None
                    if entity is Carviz:
                        social = (self.social_attitude * 2) - 1
                        matrix[x][y] += social * 0.4
                        for [_x,_y] in itertools.product([-1,0,1],[-1,0,1]):
                            if _y != 0 and _x != 0:
                                try:
                                    matrix[x+_x][y+_y] += social * 0.2
                                except IndexError:
                                    pass
                    if entity is Erbast:
                        matrix[x][y] = -5
                        for [_x,_y] in itertools.product([-2,-1,0,1,2],[-2,-1,0,1,2]):
                            if _y != 0 and _x != 0:
                                try:
                                    matrix[x+_x][y+_y] += 0.25
                                except IndexError:
                                    pass
            matrix = np.array(matrix)[1:4, 1:4]
            highest = [-10, 0,0]
            for x in range(matrix.shape[0]):
                for y in range(matrix.shape[1]):
                    if matrix[x][y] > highest[0]:
                        highest[0] = matrix[x][y]
                        highest[1] = x-1
                        highest[2] = 1-y
            return Move([highest[1], highest[2]])
        else:
            map = map[1:4,1:4]
            erbast = []
            for x in range(map.shape[0]):
                for y in range(map.shape[1]):
                    tile = map[x][y]
                    print(tile)
                    try:
                        entity = tile.entity[0] is Erbast
                    except IndexError:
                        entity = None
                        print(tile.entity)
                    if entity is Erbast:
                        erbast.append([x,y])
            if len(erbast) != 0:
                coords = random.choice(erbast)
                return Attack([coords[0]-1, 1-coords[1]])

class Erbast: # Yellow
    def __init__(self, energy=100, social_attitude=0.5) -> None:
        self.energy = energy
        self.max_energy = 100
        self.age = 0
        self.social_attitude = social_attitude
        self.color = 3

    def set_energy(self, x, add=False):
        if add == False:
            self.energy = x
        else:
            self.energy += x
        if self.energy > self.max_energy:
            self.energy = self.max_energy

    def _age(self):
        self.age += 1
        if self.age % 10 == 0:
            self.max_energy -= AGING

    def decide(self, map) -> Decision:
        self._age()
        matrix = [[random.uniform(0.20, 0.40) for _ in range(5)] for _ in range(5)]
        matrix[2][2] = -0.15
        for x in range(map.shape[0]):
            for y in range(map.shape[1]):
                try:
                    entity = map[x][y].entity[0]
                except IndexError:
                    entity = None
                if entity is Carviz:
                    matrix[x][y] = -5
                    for [_x,_y] in itertools.product([-2,-1,0,1,2],[-2,-1,0,1,2]):
                        if _y != 0 and _x != 0:
                            try:
                                matrix[x+_x][y+_y] -= 0.35
                            except IndexError:
                                pass
                if map[x][y].vegetob is not None:
                    energy = 1 - (self.energy / 100)
                    matrix[x][y] += energy * 0.4
                    for [_x,_y] in itertools.product([-1,0,1],[-1,0,1]):
                        if _y != 0 and _x != 0:
                            try:
                                matrix[x+_x][y+_y] += energy * 0.45
                            except IndexError:
                                pass
                if entity is Erbast:
                    social = (self.social_attitude * 2) - 1
                    matrix[x][y] += social * 0.4
                    for [_x,_y] in itertools.product([-1,0,1],[-1,0,1]):
                        if _y != 0 and _x != 0:
                            try:
                                matrix[x+_x][y+_y] += social * 0.2
                            except IndexError:
                                pass

        matrix = np.array(matrix)[1:4, 1:4]
        highest = [-10, 0,0]
        for x in range(matrix.shape[0]):
            for y in range(matrix.shape[1]):
                if matrix[x][y] > highest[0]:
                    highest[0] = matrix[x][y]
                    highest[1] = x-1
                    highest[2] = 1-y
        if highest[1] == 0 and highest[2] == 0:
            return Graze()
        else:
            return Move([highest[1], highest[2]])
