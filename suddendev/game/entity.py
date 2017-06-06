from .vector import Vector
from .game_config import GameConfig as gc

def entity_init(self):
    self.tag = 0
    self.pos = gc.E_POS
    self.vel = gc.E_VEL
    self.speed = gc.E_SPEED
    self.size = gc.E_SIZE
    self.healthMax = gc.E_HEALTHMAX
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
        if name != 'dummy':
            self.dummy.__setattr__(name, value)

    def injure(self, damage):
        if (damage > 0):
            self.health = max(0, self.health - damage)

    def update(self, delta):
        return self.pos + self.vel * delta
