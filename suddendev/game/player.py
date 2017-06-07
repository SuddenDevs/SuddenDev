from .entity import Entity
from .vector import Vector
from .powerup import PowerupType
from .sandbox import builtins
from .color import Color3
from .util import (
        distance_to,
        move_to,
        move_from,
        move_to_pos,
        move_from_pos,
        get_nearest,
        get_farthest
        )

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
        self.speed = self.game.gc.P_SPEED
        self.range_visible = self.game.gc.P_RANGE_VISIBLE
        self.range_attackable = self.game.gc.P_RANGE_ATTACKABLE
        self.ammo = self.game.gc.P_AMMO
        self.damage = self.game.gc.P_DAMAGE

        self.attack_delay = self.game.gc.P_ATTACK_DELAY
        self.attack_timer = 0

        if not self.try_apply_script(script, game):
            self.try_apply_script(self.game.gc.P_DEFAULT_SCRIPT, game)

    def reset_dummy(self):
        self.dummy.name = self.name 
        self.dummy.color = self.color 
        self.dummy.vel = self.vel 
        self.dummy.game = self.game 
        self.dummy.speed = self.speed
        self.dummy.range_visible = self.range_visible
        self.dummy.range_attackable = self.range_attackable
        self.dummy.damage = self.damage 
        self.dummy.attack_timer = self.attack_timer
        self.dummy.attack_delay = self.attack_delay

    def powerups_visible(self):
        in_range = []
        for p in self.game.powerups:
            d = Vector.Length(p.pos - self.pos)
            if d <= self.range_visible:
                in_range.append(p)
        return in_range                

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
            'PowerupType' : PowerupType,
            'core' : game.core,
            'random' : random,
            'sys' : sys,
            'shoot' : shoot,

            'move_to' : move_to,
            'move_from' : move_from,
            'move_to_pos' : move_to_pos,
            'move_from_pos' : move_from_pos,
            'get_nearest' : get_nearest,
            'get_farthest' : get_farthest,
            'distance_to' : distance_to,

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
        if 'update' in self.scope:
            update = self.scope['update']
            if callable(update) and len(inspect.signature(update).parameters) == 2:
                #Create dummy function in special scope
                self.script_update = type(update)(update.__code__, self.scope)
                return True
        return False

    def update(self, delta):
        #Perform player-specific movement calculation
        self.scope['enemies_visible'] = self.enemies_visible()
        self.scope['enemies_attackable'] = self.enemies_attackable()
        self.scope['powerups_visible'] = self.powerups_visible()

        if self.attack_timer > 0:
            self.attack_timer -= 1

        #Execute on Dummy Entity
        self.script_update(self.dummy, delta)

        #Check for sanity (restrict velocity)
        if Vector.Length(self.dummy.vel) > self.speed:
            self.dummy.vel = Vector.Normalize(self.dummy.vel) * self.speed

        self.vel = self.dummy.vel
        # Have to update this because shoot() runs on the dummy
        self.attack_timer = self.dummy.attack_timer
        self.ammo = self.dummy.ammo

        #Reset dummy
        self.reset_dummy()

        #Apply Motion
        return super().update(delta)

    def __str__(self):
        return str(self.name) + ":" + str(self.pos)

# TODO: This should be restricted to the dummy and access the real player's
# damage for verification, otherwise someone could do:
# 
# self.damage = 999999999
# shoot(self, enemy)
def shoot(player, enemy):
    if (Vector.Distance(enemy.pos, player.pos) <= player.range_attackable
            and player.ammo > 0 and player.attack_timer == 0):
        # Point towards the target
        player.vel = enemy.pos - player.pos
        player.vel = Vector.Normalize(player.vel) * 0.01

        # Deal damage
        player.ammo -= 1
        enemy.injure(player.damage)

        player.attack_timer = player.attack_delay
