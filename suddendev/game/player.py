from .entity import Entity
from .vector import Vector
import math
import random
import inspect

DEFAULT_SCRIPT_2 = """
timer = 1

def update(self, delta):
    self.vel = Vector(random.random(), random.random())
    # self.locals['timer'] += delta
    # if self.locals['timer'] > 2:
        # self.vel = Vector.Normalize(Vector(random.random()-0.5, random.random()-0.5)) * self.speed
        # self.locals['timer']  = 0
"""

DEFAULT_SCRIPT = """
class Controller:
    def __init__(self):
        self.timer = 0
        pass

    def update(self, player, delta):
        self.timer += delta
        player.vel = Vector(random.random(), random.random())
"""

class Player(Entity):
    def __init__(self, name, color, game, script):
        super().__init__()
        self.name = name
        self.color = color
        self.vel = Vector(random.random(), random.random())
        self.game = game
        self.speed = 20
        self.code = None

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

        #Compile supplied script
        self.script = compile(script, str(self.name), 'exec')

        #Execute in the context of the special namespace
        locals = {}
        exec(self.script, self.scope, locals)

        #Find class, check update method existence and signature
        player_class = None
        for k, v in locals.items():
            if inspect.isclass(v):
                print('Found class: ' + k)
                update = getattr(v, 'update', None)
                if callable(update):
                    if len(inspect.signature(update).parameters) == 3:
                        print('Right signature')
                        self.code = v()
                        return True
        return False

    def update(self, delta):
        #Perform player-specific movement calculation
        #Execute on Dummy Entity
        self.code.update(self.dummy, delta)

        #Check for sanity (restrict velocity)
        self.vel = self.dummy.vel

        #Reset dummy

        #Apply Motion
        super().update(delta)

    def __str__(self):
        return str(self.name) + ":" + str(self.pos)
