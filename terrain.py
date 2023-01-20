import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
from noise import snoise2
import random

class Terrain:
    def __init__(self, width = 100, height = 100, scale = 35, octaves = 16, persistence = 0.7, lacunarity = 1.6):
        self.width = width
        self.height = height
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.terrain = np.zeros((width, height))
        self.fig, self.ax = plt.subplots()
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1) # TODO: Adjust the alignment

    def next(self, _): # _ is an event object and we don't use it
        self.terrain = np.zeros((self.width, self.height))
        self.generate()
        self.l.set_data(self.terrain)
        plt.draw()

    def generate(self):
        base = random.SystemRandom().randint(0, 10000)
        # For each row in the terrain array
        for x in range(self.width):
			# For each column in the terrain array
            for y in range(self.height):
				# Get the noise value for that position
                self.terrain[x][y] = snoise2(x / self.scale,
                                 y / self.scale,
                                 octaves= self.octaves,
                                 persistence=self.persistence,
                                 lacunarity=self.lacunarity,
                                 repeatx=self.width,
                                 repeaty=self.height,
                                 base=base)

	# Normalize the data so that it is between 0 and 1
        self.terrain = (self.terrain + 1) / 2

        # Round the data to 0 or 1
        self.terrain = np.where(self.terrain > 0.5, 1, 0)
        return self

    def show(self):
        self.l = self.ax.imshow(self.terrain, cmap='BuGn') # type: ignore imshow type stuff not important # TODO: Make 0 values blue and 1 values green
        axbutton = plt.axes([0.8, 0.05, 0.1, 0.075])
        button = Button(axbutton, 'Re-plot')
        button.on_clicked(self.next)
        plt.show()
        return self
