from .entity import Entity
from .vector import Vector
from .sandbox import builtins

import math
import random
import sys
import inspect

DEFAULT_SCRIPT = """
timer = 0

def update(player, delta):
    global timer
    timer += delta

    # Find Target
    min_dist = sys.float_info.max
    target = None
    for e in enemies_visible:
        mag = Vector.Length(e.pos - player.pos)
        if mag < min_dist:
            min_dist = mag
            target = e

    if target is not None:
        diff = player.pos - target.pos
        mag = min(player.speed, min_dist)
        player.vel = Vector.Normalize(diff) * mag
    else:
        player.vel = Vector(0,0)
"""

class Player(Entity):
    def __init__(self, name, color, game, script):
        super().__init__()
        self.name = name
        self.color = color
        self.vel = Vector(random.random(), random.random())
        self.game = game
        self.speed = 20
        self.range_visible = 50
        self.range_attackable = 30

        if not self.try_apply_script(script, game):
            self.try_apply_script(DEFAULT_SCRIPT, game)

    def enemies_visible(self):
        in_range = []
        for e in self.game.enemies:
            d = Vector.Length(e.pos - self.pos)
            if d <= self.range_visible:
                in_range.append(e)
        return in_range                

    def enemies_attackable(self):
        in_range = []
        for e in self.game.enemies:
            d = Vector.Length(e.pos - self.pos)
            if d <= self.range_attackable:
                in_range.append(e)
        return in_range                

    def try_apply_script(self, script, game):
        if script is None:
            return False

        self.scope = {
            'math' : math,
            'Vector' : Vector,
            'core' : game.core,
            'random' : random,
            'sys' : sys,
            '__builtins__' : builtins
        }

        exec(script, self.scope)
        print(self.scope)

        # Check update method existence and signature of update function
        update = self.scope['update']
        if update is not None and callable(update):
            if len(inspect.signature(update).parameters) == 2:
                #Create dummy function in special scope
                self.script_update = type(update)(update.__code__, self.scope)
                return True
        return False

    def update(self, delta):
        #Perform player-specific movement calculation
        self.scope['enemies_visible'] = self.enemies_visible()
        self.scope['enemies_attackable'] = self.enemies_attackable()

        #Execute on Dummy Entity
        self.script_update(self.dummy, delta)

        #Check for sanity (restrict velocity)
        self.vel = self.dummy.vel

        #Reset dummy

        #Apply Motion
        super().update(delta)

    def __str__(self):
        return str(self.name) + ":" + str(self.pos)
