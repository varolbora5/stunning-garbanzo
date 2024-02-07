class Vegetob(): # DarkGreen
    def __init__(self, density) -> None:
        self.density = density

    def get_density(self):
        return self.density

    def grow(self):
        if self.density < 100:
            self.density += 1
        return self

class Carviz(): # Red
    def __init__(self) -> None:
        self.energy = 0
        self.lifetime = 100
        self.age = 0
        self.social = 0.5

    def decide(self, map):
        pass

class Erbast: # Yellow
    def __init__(self) -> None:
        self.energy = 0
        self.lifetime = 100
        self.age = 0
        self.social = 0.5
