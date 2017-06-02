from .vector import Vector

class Entity:
    def __init__(self):
        self.tag = 0
        self.pos = Vector(0, 0)
        self.vel = Vector(0, 0)
        self.speed = 10
        self.size = 10
        self.healthMax = 100
        self.health = self.healthMax

    def injure(self, damage):
        if (damage > 0):
            self.health = max(0, self.health - damage)

    def update(self, delta):
        self.pos = self.pos + self.vel * delta
