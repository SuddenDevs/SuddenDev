from .vector import Vector

def entity_init(self):
    self.tag = 0
    self.pos = Vector(0, 0)
    self.vel = Vector(0, 0)
    self.speed = 10
    self.size = 10
    self.healthMax = 100
    self.health = self.healthMax

class Dummy():
    def __init__(self):
        entity_init(self)

class Entity():
    def __init__(self):
        self.dummy = Dummy()
        entity_init(self)

    #Forward property changes to dummy
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        # if name != 'dummy':
            # self.dummy.__setattr__(name, value)

    def injure(self, damage):
        if (damage > 0):
            self.health = max(0, self.health - damage)

    def update(self, delta):
        self.pos = self.pos + self.vel * delta
