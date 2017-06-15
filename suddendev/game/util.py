from .vector import Vector
from .entity import Entity, Dummy
from .message import Message
from .event import Event, EventType
from .enemy_type import EnemyType
from .color import Color3
from .path import Path
import sys
import signal
import traceback

# Prints a message to the console.
def user_print(self, message):
    if self is None or message is None:
        return

    self.game.events_add(Event(EventType.PRINT, str(message), self))

def shoot(self, enemy):
    _shoot(self, enemy, is_player=True)

def enemy_shoot(self, enemy):
    _shoot(self, enemy, is_player=False)

def _shoot(self, enemy, is_player):
    if self is None or enemy is None:
        return

    enemy = self.game.find_by_tag(enemy.tag)
    if enemy is None:
        return

    # What is dead may never die
    if enemy.health <= 0:
        return

    if (Vector.Distance(enemy.pos, self.pos) <= self.range_attackable and self.attack_timer == 0):
        if not is_player or self.ammo > 0:
            # Point towards the target
            self.vel = enemy.pos - self.pos
            self.vel = Vector.Normalize(self.vel) * 0.01

            if is_player:
                self.ammo -= 1

            # Deal damage
            enemy.injure(self.damage)

            # Cool down
            self.attack_timer = self.attack_delay

            # Add event
            self.game.events_add(Event(EventType.ATTACK, self, enemy))

            from .enemy import Enemy
            if isinstance(enemy, Enemy) and enemy.health <= 0:
                self.game.stats[self.player_id]['kills'] += 1

# Broadcasts a message to all players, excluding the sender. string has to be
# set in order for the message to be sent. If only one argument is provided as
# the body, the argument is unpacked from a list to the object itself for convenience.
def say(self, string, *body):
    _say(self, string, False, body)

# Broadcasts a message to all players, including the sender.
def say_also_to_self(self, string, *body):
    _say(self, string, True, body)

def _say(self, string, to_self, body):
    if self is not None and string is not None:
        # Limit how many messages can be sent per frame.
        if self.message_count >= self.message_limit:
            return

        self.message_count += 1

        if len(body) == 1:
            body = body[0]
        msg = Message(source=self, string=string, to_self=to_self, body=body)
        self.game.events_add(Event(EventType.MESSAGE_SENT, msg))

        for p in self.game.players:
            if p.script_respond is None:
                continue
            # Only respond to own message if it's marked as such
            if to_self or p is not self:
                try:
                    signal.alarm(self.game.gc.SCRIPT_TIMEOUT)
                    p.script_respond(p.dummy, msg)
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
                    p.script_respond = None

# Returns distance from self to the target's position.
def distance_to(self, target):
    if self is None or target is None:
        return sys.maxsize

    if isinstance(target, Entity):
        target = target.pos
    elif isinstance(target, Dummy):
        target = self.game.find_by_tag(target.tag)
        if target is not None:
            target = target.pos
        else:
            return sys.maxsize
    elif not isinstance(target, Vector):
        return sys.maxsize

    return Vector.Distance(self.pos, target)

# Sets the velocity vector, scaled to the given speed, pointing to the target.
# If speed is not given, defaults to self.speed.
def move_to(self, target, speed=None):
    if self is None or target is None:
        #user_print(self, '\'None\' type passed to move_to')
        return

    if isinstance(target, Entity):
        target = target.pos
    elif isinstance(target, Dummy):
        target = self.game.find_by_tag(target.tag)
        if target is not None:
            target = target.pos
        else:
            return
    elif not isinstance(target, Vector):
        return

    if speed is None:
        speed = self.speed

    # Prevent spazzing out
    if is_at(self.pos, target):
        speed = 0.01

    self.vel = Vector.Normalize(target - self.pos) * speed

def move_from(self, target, speed=None):
    if self is None or target is None:
        return

    if isinstance(target, Entity):
        target = target.pos
    elif not isinstance(target, Vector):
        return

    if speed is None:
        speed = self.speed

    self.vel = Vector.Normalize(self.pos - target) * speed

# Gets nearest enemy within visible range.
def get_nearest_enemy(self, enemy_type=None):
    if enemy_type is None:
        return get_nearest(self, self.enemies_visible())
    else:
        enemies = self.enemies_visible()
        valid = []
        for e in enemies:
            if e.enemy_type == enemy_type:
                valid.append(e)
        return get_nearest(self, valid)

# Gets nearest enemy within attackable range.
def get_nearest_attackable_enemy(self, enemy_type=None):
    if enemy_type is None:
        return get_nearest(self, self.enemies_attackable())
    else:
        enemies = self.enemies_attackable()
        valid = []
        for e in enemies:
            if e.enemy_type == enemy_type:
                valid.append(e)
        return get_nearest(self, valid)

# Gets nearest pickup of the given type, or of any type if none is given.
def get_nearest_pickup(self, pickup_type=None):
    if pickup_type is None:
        return get_nearest(self, self.pickups_visible())
    else:
        pickups = self.pickups_visible()
        valid = []
        for p in pickups:
            if p.pickup_type == pickup_type:
                valid.append(p)
        return get_nearest(self, valid)

# Given self and a list of entities, returns the nearest entity and the 
# distance to that entity
def get_nearest(self, entities, with_distance=False):
    if self is None or entities is None:
        if with_distance:
            return None, sys.maxsize
        else:
            return None

    nearest_distance = sys.maxsize
    nearest = None

    for e in entities:
        distance = Vector.Distance(self.pos, e.pos)
        if distance < nearest_distance:
            nearest = e
            nearest_distance = distance

    if with_distance:
        return nearest, nearest_distance
    else:
        return nearest

# Given self and a list of entities, returns the farthest entity and the 
# distance to that entity
def get_farthest(self, entities, with_distance=False):
    if self is None or entities is None:
        if with_distance:
            return None, -1
        else:
            return None

    farthest_distance = -1
    farthest = None

    for e in entities:
        distance = Vector.Distance(self.pos, e.pos)
        if distance > farthest_distance:
            farthest = e
            farthest_distance = distance

    if with_distance:
        return farthest, farthest_distance
    else:
        return farthest

# Moves according to the given path. If loop is true, will go back to the beginning
# once the end of the path is reached.
def follow_path(self, path, loop=False):
    if self is None or not isinstance(path, Path) or path.is_empty():
        return

    target = path.current_target()
    move_to(self, target)
    if is_at(self.pos, path.current_target()):
        path.set_next_target(loop)

def is_at(v1, v2):
    if v1 is None or v2 is None:
        return False

    distance_thresh = 3
    return Vector.Distance(v1, v2) <= distance_thresh
