from .entity import Entity
from .vector import Vector
import random

class Player(Entity):
    def __init__(self, name, color):
        super().__init__()
        self.name = name
        self.color = color
        self.vel = Vector(random.random(), random.random())

    def update(self, delta):
        #Perform player-specific movement calculation
        #Check for sanity (restrict velocity)
        
        #Apply Motion
        super().update(delta)

    def __str__(self):
        return str(self.name) + ":" + str(self.pos)

