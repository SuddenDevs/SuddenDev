from .entity import Entity
from .vector import Vector
import math
import random

DEFAULT_SCRIPT = """
timer = 1

def update(self, delta):
    self.locals['timer'] += delta
    print(self.locals['timer'])
    if self.locals['timer'] > 2:
        self.vel = Vector.Normalize(Vector(random.random()-0.5, random.random()-0.5)) * self.speed
        self.locals['timer']  = 0
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
                'math' : math,
                'Vector' : Vector,
                'core' : game.core,
                'random' : random,
                'enemies' : game.enemies
            }
        self.locals = {}

        #Compile supplied script
        self.script = compile(script, str(self.name), 'exec')

        #Execute in the context of the special namespace
        exec(self.script, self.scope, self.locals)

        return 'update' in self.locals

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
