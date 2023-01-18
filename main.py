import matplotlib as pl
import numpy as np
import pandas as pd

from species import Vegetob
from terrain import Terrain

if __name__ == "__main__":
	world = Terrain()
	world.generate()

	world.show()