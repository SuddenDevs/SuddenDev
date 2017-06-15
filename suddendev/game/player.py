from .entity import Entity
from .vector import Vector
from .pickup import PickupType
from .sandbox import builtins
from .color import Color3
from .event import Event, EventType
from .util import *
from .game_config import GameConfig as gc
from .enemy_type import EnemyType

from functools import partial

import math
import random
import sys
import inspect
import signal
import traceback

class Player(Entity):
    def __init__(self, name, color, game, script, player_id):
        super().__init__()
        self.player_id = player_id
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

        self.message_limit = self.game.gc.P_MESSAGE_LIMIT
        self.message_count = 0

        # Register the handler for timing out user scripts
        signal.signal(signal.SIGALRM, timeout_handler)

        if not self.try_apply_script(script, self.game):
            self.try_apply_script(self.game.gc.P_ERROR_SCRIPT, self.game)

    def reset_dummy(self):
        self.dummy.tag = self.tag 
        self.dummy.pos = self.pos 
        self.dummy.vel = self.vel 
        self.dummy.speed = self.speed 
        self.dummy.size = self.size 
        self.dummy.health = self.health 
        self.dummy.healthMax = self.healthMax 

        self.dummy.name = self.name 
        self.dummy.color = self.color 
        self.dummy.range_visible = self.range_visible
        self.dummy.range_attackable = self.range_attackable

        self.dummy.damage = self.damage 
        self.dummy.attack_delay = self.attack_delay
        self.dummy.attack_timer = self.attack_timer
        self.dummy.ammo = self.ammo

        self.dummy.message_limit = self.message_limit
        self.dummy.message_count = 0

    def get_in_range(self, entities, dist):
        in_range = []
        for p in entities:
            if distance_to(self, p) <= dist:
                in_range.append(p)
        return in_range                

    def pickups_visible(self):
        return self.get_in_range(self.game.pickups, self.range_visible)

    def enemies_visible(self):
        return self.get_in_range(self.game.enemies, self.range_visible)

    def enemies_attackable(self):
        return self.get_in_range(self.game.enemies, self.range_attackable)

    def try_apply_script(self, script, game):
        if script is None:
            return False

        self.scope = {
            'math' : math,
            'Vector' : Vector,
            'PickupType' : PickupType,
            'EnemyType' : EnemyType,
            'core' : game.core,
            'random' : random,
            'sys' : sys,

            'say' : partial(say, self),
            'say_also_to_self' : partial(say_also_to_self, self),
            'shoot' : partial(shoot, self),
            'move_to' : partial(move_to, self),
            'move_from' : partial(move_from, self),
            'get_nearest' : partial(get_nearest, self),
            'get_nearest_enemy' : partial(get_nearest_enemy, self),
            'get_nearest_attackable_enemy' : partial(get_nearest_attackable_enemy, self),
            'get_nearest_pickup' : partial(get_nearest_pickup, self),
            'get_farthest' : partial(get_farthest, self),
            'distance_to' : partial(distance_to, self),
            'print' : partial(user_print, self),

            '__builtins__' : builtins
        }

        # If the script throws an error, just give up
        try:
            signal.alarm(self.game.gc.SCRIPT_TIMEOUT)
            exec(script, self.scope)
            signal.alarm(0)
        except Exception:
            # Format traceback
            exp, val, tb = sys.exc_info()
            listing = traceback.format_exception(exp, val, tb)

            del listing[0]
            del listing[0]
            # Set color to red to signify the bot is broken
            self.game.events_add(Event(EventType.ERROR, listing, self))
            self.color = Color3(255,0,0)
            return False

        # Check update method existence and signature of update function
        self.script_respond = None
        if 'respond' in self.scope:
            respond = self.scope['respond']
            if callable(respond) and len(inspect.signature(respond).parameters) == 2:
                #Create dummy function in special scope
                self.script_respond = type(respond)(respond.__code__, self.scope)
        if 'update' in self.scope:
            update = self.scope['update']
            if callable(update) and len(inspect.signature(update).parameters) == 2:
                #Create dummy function in special scope
                self.script_update = type(update)(update.__code__, self.scope)
                return True
        return False

    def update(self, delta):
        # Update what the player knows about the world
        self.update_game_state_info()

        if self.attack_timer > 0:
            self.attack_timer -= 1

        self.message_count = 0

        # Execute on Dummy Entity
        try:
            signal.alarm(self.game.gc.SCRIPT_TIMEOUT)
            self.script_update(self.dummy, delta)
            signal.alarm(0)
        except Exception:
            # If script is broken, set color to red to signify the bot is broken
            # and reset to error script
            # Format traceback
            exp, val, tb = sys.exc_info()
            listing = traceback.format_exception(exp, val, tb)

            del listing[0]
            del listing[0]
            # Set color to red to signify the bot is broken
            self.game.events_add(Event(EventType.ERROR, listing, self))
            self.color = Color3(255,0,0)
            self.try_apply_script(self.game.gc.P_ERROR_SCRIPT, self.game)

        # Check for sanity (restrict velocity)
        if Vector.Length(self.dummy.vel) > self.speed:
            self.dummy.vel = Vector.Normalize(self.dummy.vel) * self.speed

        self.vel = self.dummy.vel

        # Reset dummy
        self.reset_dummy()

        # Apply Motion
        return super().update(delta)

    def update_game_state_info(self):
        self.scope['enemies_visible'] = self.enemies_visible()
        self.scope['enemies_attackable'] = self.enemies_attackable()
        self.scope['pickups_visible'] = self.pickups_visible()

    def __str__(self):
        return str(self.name) + ":" + str(self.pos)

class TimeoutException(Exception):
    pass

# Handler for SIGALRM for timing out user scripts.
def timeout_handler(signum, frame):
    raise TimeoutException('Function timed out. Allowed time for functions is ' +
            str(gc.SCRIPT_TIMEOUT) + ' second.')
