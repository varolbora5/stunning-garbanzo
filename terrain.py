import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
from noise import snoise2
import random

class Tile():
    def __init__(self, land) -> None:
        self.land = land
        self.entity = None



class Terrain:
    def __init__(self, width = 100, height = 100, scale = 35, octaves = 16, persistence = 0.7, lacunarity = 1.6):
        self.width = width
        self.height = height
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.terrain = np.full((width, height), Tile(0))
        self.fig, self.ax = plt.subplots()
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1) # TODO: Adjust the alignment

    def next(self, _): # _ is an event object and we don't use it
        self.terrain = np.full((self.width, self.height), Tile(0))
        self.generate()
        self.l.set_data([[y.land for y in x] for x in self.terrain])
        plt.draw()

    def generate(self):
        base = random.SystemRandom().randint(0, 10000)
        # For each row in the terrain array
        for row in self.terrain:
            # For each column in the terrain array
            for tile in row:
                # Get the noise value for that position
                tile.land = snoise2(x / self.scale,
                                             y / self.scale,
                                             octaves= self.octaves,
                                             persistence=self.persistence,
                                             lacunarity=self.lacunarity,
                                             repeatx=self.width,
                                             repeaty=self.height,
                                             base=base)

    # Normalize the data so that it is between 0 and 1
        for row in self.terrain:
            for tile in row:
                tile.land = (tile.land + 1) / 2

        # Round the data to 0 or 1

        for row in self.terrain:
            for tile in row:
                if tile.land > 0.5:
                    tile.land = 1
                else:
                    tile.land = 0

        return self


        # map = [[0]*self.height]*self.width
        # for row, i in self.terrain:
        #     for tile, j in row:
        #         map[i][j] = tile.land


    def show(self):
        self.l = self.ax.imshow( [[y.land for y in x] for x in self.terrain], cmap='BuGn') # type: ignore imshow type stuff not important # TODO: Make 0 values blue and 1 values green
        axbutton = plt.axes([0.8, 0.05, 0.1, 0.075])
        button = Button(axbutton, 'Re-plot')
        button.on_clicked(self.next)
        plt.show()
        return self
