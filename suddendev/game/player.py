from .entity import Entity
from .vector import Vector
from .sandbox import builtins
from .color import Color3
from .game_config import GameConfig as gc

import math
import random
import sys
import inspect

class Player(Entity):
    def __init__(self, name, color, game, script):
        super().__init__()
        self.name = name
        self.color = color
        self.vel = Vector(random.random(), random.random())
        self.game = game

        self.speed = gc.P_SPEED
        self.range_visible = gc.P_RANGE_VISIBLE
        self.range_attackable = gc.P_RANGE_ATTACKABLE
        self.ammo = gc.P_AMMO
        self.damage = gc.P_DAMAGE

        # Flag to ensure we only attack once per frame
        self.attacked = False

        if not self.try_apply_script(script, game):
            self.try_apply_script(gc.P_DEFAULT_SCRIPT, game)

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
        print(script)
        if script is None:
            return False

        self.scope = {
            'math' : math,
            'Vector' : Vector,
            'core' : game.core,
            'random' : random,
            'sys' : sys,
            'shoot' : shoot,
            '__builtins__' : builtins
        }

        # If the script throws an error, just give up
        # TODO: Inform user somehow
        try:
            exec(script, self.scope)
        except:
            # Set color to red to signify the bot is broken
            self.color = Color3(255,0,0)
            return False

        # Check update method existence and signature of update function
        if 'update' not in self.scope:
            return False

        update = self.scope['update']
        if update is not None and callable(update):
            if len(inspect.signature(update).parameters) == 2:
                #Create dummy function in special scope
                self.script_update = type(update)(update.__code__, self.scope)
                return True
        return False

    def update(self, delta):
        self.attacked = False

        #Perform player-specific movement calculation
        self.scope['enemies_visible'] = self.enemies_visible()
        self.scope['enemies_attackable'] = self.enemies_attackable()

        #Execute on Dummy Entity
        self.script_update(self.dummy, delta)

        #Check for sanity (restrict velocity)
        self.vel = self.dummy.vel

        #Reset dummy

        #Apply Motion
        return super().update(delta)

    def __str__(self):
        return str(self.name) + ":" + str(self.pos)

def shoot(player, enemy):
    if Vector.Distance(enemy.pos, player.pos) <= player.range_attackable and player.ammo > 0 and not player.attacked:
        # Point towards the target
        player.vel = enemy.pos - player.pos
        player.vel = Vector.Normalize(player.vel) * 0.01

        # Deal damage
        player.ammo -= 1
        enemy.injure(player.damage)

        player.attacked = True
