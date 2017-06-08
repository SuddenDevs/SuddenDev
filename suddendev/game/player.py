from .entity import Entity
from .vector import Vector
from .powerup import PowerupType
from .sandbox import builtins
from .color import Color3
from .event import Event, EventType
from .util import (
        user_print,
        shoot,
        say,
        say_also_to_self,
        distance_to,
        move_to,
        move_from,
        move_to_pos,
        move_from_pos,
        get_nearest,
        get_farthest
        )
from .message import Message
from .game_config import GameConfig as gc

import math
import random
import sys
import inspect
import signal
import traceback

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

        self.has_message = False
        self.message = None

        # Register the handler for timing out user scripts
        signal.signal(signal.SIGALRM, timeout_handler)

        if not self.try_apply_script(script, self.game):
            self.try_apply_script(self.game.gc.P_DEFAULT_SCRIPT, self.game)

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
        self.dummy.vel = self.vel 
        self.dummy.speed = self.speed
        self.dummy.range_visible = self.range_visible
        self.dummy.range_attackable = self.range_attackable

        self.dummy.damage = self.damage 
        self.dummy.attack_delay = self.attack_delay

        self.has_message = False
        self.message = None

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

            'say' : say,
            'say_also_to_self' : say_also_to_self,
            'shoot' : shoot,
            'move_to' : move_to,
            'move_from' : move_from,
            'move_to_pos' : move_to_pos,
            'move_from_pos' : move_from_pos,
            'get_nearest' : get_nearest,
            'get_farthest' : get_farthest,
            'distance_to' : distance_to,
            'print' : user_print,

            '__builtins__' : builtins
        }

        # If the script throws an error, just give up
        # TODO: Inform user somehow
        try:
            signal.alarm(self.game.gc.SCRIPT_TIMEOUT)
            exec(script, self.scope)
            signal.alarm(0)
        except Exception:
            # Set color to red to signify the bot is broken
            self.game.add_error(traceback.format_exc())
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

        # Execute on Dummy Entity
        try:
            signal.alarm(self.game.gc.SCRIPT_TIMEOUT)
            self.script_update(self.dummy, delta)
            signal.alarm(0)
        except Exception:
            # If script is broken, set color to red to signify the bot is broken
            # and reset to default script
            # TODO: Send an event and stack trace
            self.game.add_error(traceback.format_exc())
            self.color = Color3(255,0,0)
            self.try_apply_script(self.game.gc.P_DEFAULT_SCRIPT, self.game)

        # Check for sanity (restrict velocity)
        if Vector.Length(self.dummy.vel) > self.speed:
            self.dummy.vel = Vector.Normalize(self.dummy.vel) * self.speed

        self.vel = self.dummy.vel

        # TODO: way to fix this?
        # Have to update this because shoot() runs on the dummy
        self.attack_timer = self.dummy.attack_timer
        self.ammo = self.dummy.ammo

        # Send message if there's one to be sent
        self.send_message_if_needed()

        # Reset dummy
        self.reset_dummy()

        # Apply Motion
        return super().update(delta)

    def update_game_state_info(self):
        self.scope['enemies_visible'] = self.enemies_visible()
        self.scope['enemies_attackable'] = self.enemies_attackable()
        self.scope['powerups_visible'] = self.powerups_visible()

    def send_message_if_needed(self):
        # If there's a message to be sent, have everyone respond
        if self.dummy.has_message and self.dummy.message is not None:
            self.game.events_add(Event(EventType.MESSAGE_SENT, self.dummy.message))
            for p in self.game.players:
                if p.script_respond is None:
                    continue
                # Only respond to own message if it's marked as such
                if self.dummy.message.to_self or p is not self:
                    try:
                        signal.alarm(self.game.gc.SCRIPT_TIMEOUT)
                        p.script_respond(p.dummy, self.dummy.message)
                        signal.alarm(0)
                    except Exception:
                        self.game.add_error(traceback.format_exc())
                        p.script_respond = None

    def __str__(self):
        return str(self.name) + ":" + str(self.pos)

class TimeoutException(Exception):
    pass

# Handler for SIGALRM for timing out user scripts.
def timeout_handler(signum, frame):
    raise TimeoutException('Function timed out. Allowed time for functions is ' +
            str(gc.SCRIPT_TIMEOUT) + ' seconds.')
