class Vegetob():
    def __init__(self) -> None:
        self.density = 0

    def elaborate(self):
        self.grow()

    def get_density(self):
        return self.density

    def grow(self):
        if self.density < 100:
            self.density += 1
        return self
    
class Carviz():
    def __init__(self, move) -> None:
        self.energy = 0
        self.lifetime = 100
        self.age = 0
        self.social = 0.5
        self.move = move

    def elaborate(self):
        self.age += 1
        self.move()
        return self
