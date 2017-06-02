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
        #Find Nearest Player
        ps = self.game.players
        target = ps[0].pos
        mag_min = Vector.Length(self.pos - target)
        for p in ps:
            mag = Vector.Length(self.pos - p.pos)
            if mag < mag_min:
                target = p.pos
                mag_min = mag

        to = target - self.pos
        mag = Vector.Length(to)

        self.vel = Vector.Normalize(to) * min(mag, self.speed)
        super().update(delta)
