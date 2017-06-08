from .vector import Vector
from .message import Message
from .event import Event, EventType
import sys

# TODO: This should be restricted to the dummy and access the real player's
# damage for verification, otherwise someone could do:
# 
# self.damage = 999999999
# shoot(self, enemy)
def shoot(self, enemy):
    if self is None or enemy is None:
        return

    if (Vector.Distance(enemy.pos, self.pos) <= self.range_attackable
            and self.ammo > 0 and self.attack_timer == 0):
        # Point towards the target
        self.vel = enemy.pos - self.pos
        self.vel = Vector.Normalize(self.vel) * 0.01

        # Deal damage
        self.ammo -= 1
        enemy.injure(self.damage)

        # Cool down
        self.attack_timer = self.attack_delay

        # Add event
        self.game.events_add(Event(EventType.ATTACK, self, enemy))

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
        self.has_message = True
        if len(body) == 1:
            body = body[0]
        self.message = Message(source=self, string=string, to_self=to_self, body=body)

# Returns distance from self to the target's position.
def distance_to(self, target):
    if self is None or target is None:
        return sys.maxsize

    return Vector.Distance(self.pos, target.pos)

# Sets the velocity vector, scaled to the given speed, pointing to the target.
# If speed is not given, defaults to self.speed.
def move_to_pos(self, pos, speed=None):
    if self is None or pos is None:
        return

    if speed is None:
        speed = self.speed

    self.vel = Vector.Normalize(pos - self.pos) * speed

def move_from_pos(self, pos, speed=None):
    if self is None or pos is None:
        return

    if speed is None:
        speed = self.speed

    self.vel = Vector.Normalize(self.pos - pos) * speed

def move_to(self, target, speed=None):
    if self is None or target is None:
        return

    if speed is None:
        speed = self.speed

    self.vel = Vector.Normalize(target.pos - self.pos) * speed

def move_from(self, target, speed=None):
    if self is None or target is None:
        return

    if speed is None:
        speed = self.speed

    self.vel = Vector.Normalize(self.pos - target.pos) * speed

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
