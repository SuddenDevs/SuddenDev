from .entity import Entity
from .vector import Vector
import math
import random

DEFAULT_SCRIPT = """
something = 1
someparam = 2

def update(self, delta):
    centre = core.pos
    fromCentre = Vector.Normalize(self.pos - centre) * self.speed
    self.vel = Vector.Normalize(Vector(1,1)) * self.speed
"""

class Player(Entity):
    def __init__(self, name, color, game, script):
        super().__init__()
        self.name = name
        self.color = color
        self.vel = Vector(random.random(), random.random())
        self.game = game
        self.speed = 15

        if not self.try_apply_script(script, game):
            self.try_apply_script(DEFAULT_SCRIPT, game)

    def try_apply_script(self, script, game):
        if script is None:
            return False

        self.scope = {
                'Math' : math,
                'Vector' : Vector,
                'core' : game.core,
                'enemies' : game.enemies
            }
        self.locals = {}

        #Compile supplied script
        self.script = compile(script, str(self.name), 'exec')

        #Execute in the context of the special namespace
        exec(self.script, self.scope, self.locals)

        return 'update' in self.scope

    def update(self, delta):
        #Perform player-specific movement calculation
        self.locals['update'](self, delta)
        
        #Check for sanity (restrict velocity)

        # target = self.game.core.pos
        # to = target - self.pos
        # dist = Vector.Length(to)
        # self.vel = Vector.Normalize(to) * min(dist, self.speed)
        
        #Apply Motion
        super().update(delta)

    def __str__(self):
        return str(self.name) + ":" + str(self.pos)
