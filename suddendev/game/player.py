from .entity import Entity
from .vector import Vector
import random

class Player(Entity):
    def __init__(self, name, color, game):
        super().__init__()
        self.name = name
        self.color = color
        self.vel = Vector(random.random(), random.random())
        self.game = game
        self.speed = 50

    def update(self, delta):
        #Perform player-specific movement calculation
        #Check for sanity (restrict velocity)

        target = self.game.core.pos
        to = target - self.pos
        dist = Vector.Length(to)
        self.vel = Vector.Normalize(to) * min(dist, self.speed)
        
        #Apply Motion
        super().update(delta)

    def __str__(self):
        return str(self.name) + ":" + str(self.pos)

