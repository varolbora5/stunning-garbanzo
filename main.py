import matplotlib.pyplot as plt
from species import Vegetob, Carviz
from terrain import Terrain

if __name__ == "__main__":
    world = Terrain(plt, height=420, width=420).generate().show()
    print("Program Ran Succesfully")
