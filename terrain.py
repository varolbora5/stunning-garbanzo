from matplotlib.widgets import Button
import matplotlib
import numpy as np
from noise import snoise2
import random

from species import Carviz, Erbast, Vegetob

class Tile():
    def __init__(self, land) -> None:
        self.land = land
        self.vegetob = None
        self.entity = None
        self.color = None

class Terrain:
    def __init__(self, plt, width = 300, height = 300, scale = 95, octaves = 20, persistence = 0.7, lacunarity = 1.4):
        self.plt = plt
        self.width = width
        self.height = height
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.terrain = np.full((width, height), Tile(0))
        self.map = np.zeros((width, height))
        self.fig, self.ax = self.plt.subplots()
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1) # TODO: Adjust the alignment
        self.colormap = (matplotlib.colors.ListedColormap(['#87592C', '#F75555', 'green', 'yellow', '#1DD1E2'])) #type: ignore there is a false negative about mpl.colors not existing
        self.color = None

    def next(self, _): # _ is an event object and we don't use it
        self.terrain = np.full((self.width, self.height), Tile(0))
        self.generate()
        self.l.set_data([[y.color for y in x] for x in self.terrain])
        self.plt.draw()

    def generate(self):
        base = random.SystemRandom().randint(0, 10000)
        # For each row in the terrain array
        for x in range(self.width):
            # For each column in the terrain array
            for y in range(self.height):
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
                tile.land = (tile.land + 1) / 2

        # Round the data to 0 or 1
        for row in self.terrain:
            for tile in row:
                if tile.land > 0.5:
                    tile.land = 1
                    tile.color = 0
                else:
                    tile.land = 0
                    tile.color = 4

        # Populate the terrain with entities
        self.populate()

        return self

    def show(self):
        self.l = self.ax.imshow( [[y.color for y in x] for x in self.terrain], cmap=self.colormap) # type: ignore imshow type stuff not important
        axbutton = self.plt.axes([0.8, 0.05, 0.1, 0.075])
        button = Button(axbutton, 'Re-plot')
        button.on_clicked(self.next)
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
                        tile.entity = Carviz()
                        tile.color = 1
                    elif bruh > 75:
                        tile.entity = Erbast()
                        tile.color = 3
