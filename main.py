import matplotlib.pyplot as plt
from terrain import Terrain

if __name__ == "__main__":
    world = Terrain(plt, height=100, width=100).generate().show()
    print("Program Ran Succesfully")
