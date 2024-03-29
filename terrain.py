from typing_extensions import List
from matplotlib.cbook import time
from matplotlib.widgets import Button
import typing
import matplotlib
from matplotlib import animation
import numpy as np
from noise import snoise2
import random
from consts import ATTACK_DAMAGE, REPERCUSSION_DAMAGE, ERBAST_ENERGY_GAIN, LIFETIME

from species import Attack, Carviz, Erbast, Graze, Vegetob, Decision, Move
color_list = ['black', '#F75555', 'green', 'yellow', '#1DD1E2']

def debug(*args):
    result = ""
    for arg in args:
        result += str(arg) + " "
    print(result.strip())

class Tile():
    def __init__(self, land=0, color=4) -> None:
        self.land = land
        self.vegetob = None
        self.entity = []
        self.color = color

class Terrain:
    def __init__(self, plt, width = 300, height = 300, scale = 95, octaves = 20, persistence = 0.7, lacunarity = 1.4):
        self.plt = plt
        self.width = width
        self.height = height
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.terrain = np.full((width, height), Tile(0, 4))
        self.map = np.zeros((width, height))
        self.fig, self.ax = self.plt.subplots()
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1) # TODO: Adjust the alignment
        self.colormap = (matplotlib.colors.ListedColormap(color_list)) #type: ignore there is a false negative about mpl.colors not existing
        self.anim = animation.FuncAnimation(fig=self.fig, func=self.animate, frames=np.arange(0, 60, 1), repeat=True, interval=300)
        # self.anim.pause()
        self.stop = True

    def next(self, _): # _ is an event object and we don't use it
        self.terrain = np.full((self.width, self.height), Tile(0))
        self.generate()
        self.img.set_data([[y.color for y in x] for x in self.terrain])
        self.plt.draw()

    def generate(self):
        base = random.SystemRandom().randint(0, 10000)
        # For each row in the terrain array
        for x in range(2, self.width-2):
            # For each column in the terrain array
            for y in range(2, self.height-2):
                # Get the noise value for that position
                self.terrain[x][y] = Tile(snoise2(x / self.scale,
                                             y / self.scale,
                                             octaves= self.octaves,
                                             persistence=self.persistence,
                                             lacunarity=self.lacunarity,
                                             repeatx=self.width,
                                             repeaty=self.height,
                                             base=base))

    # Normalize the data so that it is between 0 and 1
        for row in self.terrain:
            for tile in row:
                if tile.land != 0:
                    tile.land = (tile.land + 1) / 2

        # Round the data to 0 or 1
        for row in self.terrain:
            for tile in row:
                if tile.land > 0.45:
                    tile.land = 1
                    tile.color = 0
                else:
                    tile.land = 0
                    tile.color = 4

        # Populate the terrain with entities
        self.populate()

        return self

    def show(self):
        self.img = self.ax.imshow([[y.color for y in x] for x in self.terrain], cmap=self.colormap) # type: ignore imshow type stuff not important
        print(self.terrain[0][0].color)
        ax_replot_button = self.plt.axes([0.8, 0.05, 0.1, 0.075])
        replot_button = Button(ax_replot_button, 'Re-plot')
        replot_button.on_clicked(self.next)
        self.plt.show()
        return self

    def populate(self):
        for row in self.terrain:
            for tile in row:
                if tile.land == 1:
                    bruh = random.randint(1,100)
                    if bruh < 35:
                        tile.vegetob = Vegetob(random.randint(15,75))
                        tile.color = 2
                    if bruh > 20 and bruh < 45:
                        tile.entity.append(Carviz())
                        tile.color = 1
                    elif bruh > 75:
                        tile.entity.append(Erbast())
                        tile.color = 3

    def kill(self, x,y,i):
        del self.terrain[x][y].entity[i]
        try:
            if self.terrain[x][y].entity[0] is Erbast:
                self.terrain[x][y].color = 3
            elif self.terrain[x][y].entity[0] is Carviz:
                self.terrain[x][y].color = 1
        except IndexError:
            if self.terrain[x][y].vegetob is None:
                self.terrain[x][y].color = 0
            else:
                self.terrain[x][y].color = 2

    def spawn(self, x, y, energy, social_attitude):
        deviation = random.randint(0,10)
        if self.terrain[x][y].entity[0] is Carviz:
            self.terrain[x][y].entity.append(Carviz(energy/2, social_attitude + deviation))
            self.terrain[x][y].entity.append(Carviz(energy/2, social_attitude - deviation))
            self.terrain[x][y].color = 1
        else:
            self.terrain[x][y].entity.append(Erbast(energy/2, social_attitude + deviation))
            self.terrain[x][y].entity.append(Erbast(energy/2, social_attitude - deviation))
            self.terrain[x][y].color = 3

    def make_map(self,x,y):
        map = [[self.terrain[x-2][y-2],self.terrain[x-1][y-2],self.terrain[x][y-2],self.terrain[x+1][y-2],self.terrain[x+2][y-2]],
               [self.terrain[x-2][y-1],self.terrain[x-1][y-1],self.terrain[x][y-1],self.terrain[x+1][y-1],self.terrain[x+2][y-1]],
               [self.terrain[x-2][y],self.terrain[x-1][y],self.terrain[x][y],self.terrain[x+1][y],self.terrain[x+2][y]],
               [self.terrain[x-2][y+1],self.terrain[x-1][y+1],self.terrain[x][y+1],self.terrain[x+1][y+1],self.terrain[x+2][y+1]],
               [self.terrain[x-2][y+2],self.terrain[x-1][y+2],self.terrain[x][y+2],self.terrain[x+1][y+2],self.terrain[x+2][y+2]],
               ]
        _x, _y = x, y
        for x in range(5):
            for y in range(5):
                map[x][y].entity = self.terrain[_x+(x-2)][_y+(2-y)].entity
                map[x][y].vegetob = self.terrain[_x+(x-2)][_y+(2-y)].vegetob
        return np.array(map)

    def animate(self, _):
        for x in range(self.width):
            for y in range(self.height):
                if self.terrain[x][y].vegetob:
                    self.terrain[x][y].vegetob.grow()
                map = self.terrain[x-2:x+3, y-2:y+3]
                if len(self.terrain[x][y].entity) != 0 and self.terrain[x][y].land == 1:
                    amount_of_grazers = 0
                    for i in range(len(self.terrain[x][y].entity)):
                        decision: Decision = None
                        try:
                            decision = self.terrain[x][y].entity[i].decide(map)
                        except IndexError:
                            # debug(x, y, i)
                            pass
                        match decision:
                            case Move(direction):
                                self.terrain[x][y].entity[i].set_energy(-1, True)
                                same = False
                                try:
                                    same = isinstance(self.terrain[x+direction[0]][y+direction[1]].entity[0], type(self.terrain[x][y].entity[0]))
                                except IndexError:
                                    same = True
                                if same == True and self.terrain[x+direction[0]][y+direction[1]].land == 1:
                                    self.terrain[x+direction[0]][y+direction[1]].entity.append(self.terrain[x][y].entity.pop(i))
                                    if len(self.terrain[x][y].entity) < 1:
                                        if self.terrain[x][y].vegetob is None:
                                            self.terrain[x][y].color = 0
                                        else:
                                            self.terrain[x][y].color = 2
                                    self.terrain[x+direction[0]][y+direction[1]].color = self.terrain[x+direction[0]][y+direction[1]].entity[0].color
                            case Graze:
                                if self.terrain[x][y].vegetob is Vegetob:
                                    amount_of_grazers += 1
                                    self.terrain[x][y].entity[i].grazed = True
                    if amount_of_grazers != 0:
                        graze_amount = self.terrain[x][y].vegetob.get_density() / amount_of_grazers
                        for erbast in [x for x in self.terrain[x][y].entity if x.grazed == True]:
                            erbast.set_energy(int(graze_amount), True)
                            self.terrain[x][y].vegetob.set_density(0)
        for x in range(self.width):
            for y in range(self.height):
                map = self.terrain[x-2:x+3, y-2:y+3]
                if len(self.terrain[x][y].entity) == 0: continue
                for i in range(len(self.terrain[x][y].entity)):
                    if self.terrain[x][y].entity[0] is Carviz:
                        decision: Decision = None
                        try:
                            decision = self.terrain[x][y].entity[i].decide(map)
                        except IndexError:
                            # debug(x, y, i)
                            pass
                        match decision:
                            case Attack(direction):
                                direction = [0,0]
                                for _x in [-1,0,1]:
                                    for _y in [-1,0,1]:
                                        try:
                                            if self.terrain[x+_x][y+_y].entity[0] is Erbast:
                                                direction = [_x, _y]
                                        except IndexError:
                                            pass
                                if isinstance(self.terrain[x+direction[0]][y+direction[1]].entity[0], Erbast):
                                    damage = random.randint(ATTACK_DAMAGE[0], ATTACK_DAMAGE[1])
                                    if self.terrain[x+direction[0]][y+direction[1]].entity[0].energy < damage:
                                        self.terrain[x][y].entity[i].set_energy(random.randint(ERBAST_ENERGY_GAIN[0], ERBAST_ENERGY_GAIN[1]), True)
                                        self.kill(x+direction[0],y+direction[1],0)
                                    else:
                                        self.terrain[x+direction[0]][y+direction[1]].entity[0].set_energy(-damage, True)
                                        damage = random.randint(REPERCUSSION_DAMAGE[0], REPERCUSSION_DAMAGE[1])
                                        self.terrain[x][y].entity[i].set_energy(-damage, True)
                                else:
                                    pass
                            case _:
                                pass
        for x in range(self.width):
            for y in range(self.height):
                for i in range(len(self.terrain[x][y].entity)):
                    kill = False
                    killed = False
                    try:
                        kill = self.terrain[x][y].entity[i].age > LIFETIME
                        if kill:
                            self.spawn(x, y, self.terrain[x][y].entity[i].energy, self.terrain[x][y].entity[i].social_attitude)
                            self.kill(x,y,i)
                            killed = True
                    except IndexError:
                        pass
                    kill = False
                    try:
                        kill = self.terrain[x][y].entity[i].energy < 1
                        if not killed and kill:
                            self.kill(x,y,i)
                    except IndexError:
                        pass
        self.img.set(data=[[y.color for y in x] for x in self.terrain])
        # self.plt.draw()
        # for x in range(self.width):
        #     for y in range(self.height):
        #         for i in range(len(self.terrain[x][y].entity)):
        #             print(self.terrain[x][y].entity[i].energy, end=" ")
        return True
