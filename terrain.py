import matplotlib.pyplot as plt
import numpy as np
from noise import snoise2


class Terrain:
	def __init__(self, width = 100, height = 100, scale = 40, octaves = 8, persistence = 0.6, lacunarity = 2.0):
		self.width = width
		self.height = height
		self.scale = scale
		self.octaves = octaves
		self.persistence = persistence
		self.lacunarity = lacunarity
		self.terrain = np.zeros((width, height))

	def generate(self):
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
																base=0)

	# Normalize the data so that it is between 0 and 1
		self.terrain = (self.terrain + 1) / 2

	# Round the data to 0 or 1
		self.terrain = np.where(self.terrain > 0.5, 1, 0)
		return self

	def show(self):
		plt.imshow(self.terrain, cmap='Greens')
		plt.show()
		return self