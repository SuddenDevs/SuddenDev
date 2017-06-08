from .vector import Vector
from .game_config import GameConfig as gc

tag = 0

def next_tag():
    global tag
    t = tag
    tag += 1
    return t

def entity_init(self):
    self.tag = next_tag()
    self.pos = gc.E_POS
    self.vel = gc.E_VEL
    self.speed = gc.E_SPEED
    self.size = gc.E_SIZE
    self.healthMax = gc.E_HEALTHMAX
    self.health = self.healthMax
    self.vel_prev = self.vel

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
        accel = self.vel - self.vel_prev
        self.vel_prev = self.vel_prev + accel * 0.25;
        return self.pos + self.vel_prev * delta
