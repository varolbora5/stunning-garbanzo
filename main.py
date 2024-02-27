import matplotlib.pyplot as plt
from terrain import Terrain

if __name__ == "__main__":
    world = Terrain(plt, height=50, width=50).generate().show()
    print("Program Ran Succesfully")
