from .entity import Entity
from .vector import Vector

import random

class Enemy(Entity):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.pos = Vector(random.random() * self.game.map.width,
                            random.random() * self.game.map.height)
    
    def update(self, delta):
        target = Vector(self.game.map.width/2, self.game.map.height/2)
        self.vel = Vector(1,1)
