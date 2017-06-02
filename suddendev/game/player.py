from .entity import Entity
from .vector import Vector
import random

class Player(Entity):
    def __init__(self, name, color, game, script):
        super().__init__()
        self.name = name
        self.color = color
        self.vel = Vector(random.random(), random.random())
        self.game = game
        self.speed = 15

        #Create isolated namespace for player code
        #Include libraries, classes, relevant game info
        self.scope = {
                'Vector' : Vector,
                'core' : game.core,
                'enemies' : game.enemies
            }

        #Compile supplied script
        self.script = compile(script, str(name), 'exec')

        #Check for errors?

        #Execute in the context of the special namespace
        exec(self.script, self.scope)

        #Check that a function 'update(self)' has been defined
        assert self.scope['update'] is not None

    def update(self, delta):
        #Perform player-specific movement calculation
        self.scope['update'](self, delta)
        
        #Check for sanity (restrict velocity)

        # target = self.game.core.pos
        # to = target - self.pos
        # dist = Vector.Length(to)
        # self.vel = Vector.Normalize(to) * min(dist, self.speed)
        
        #Apply Motion
        super().update(delta)

    def __str__(self):
        return str(self.name) + ":" + str(self.pos)
