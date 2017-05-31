from .vector import Vector

class Entity:
    def __init__(self):
        self.tag = 0
        self.pos = Vector(0, 0)
        self.vel = Vector(0, 0)
        self.size = Vector(10, 10)
        self.healthMax = 100
        self.health = self.healthMax

    def update(self, delta):
        self.pos = self.pos + self.vel * delta

