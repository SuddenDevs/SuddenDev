from .vector import Vector
from .message import Message
import sys

# TODO: This should be restricted to the dummy and access the real player's
# damage for verification, otherwise someone could do:
# 
# self.damage = 999999999
# shoot(self, enemy)
def shoot(self, enemy):
    if (Vector.Distance(enemy.pos, self.pos) <= self.range_attackable
            and self.ammo > 0 and self.attack_timer == 0):
        # Point towards the target
        self.vel = enemy.pos - self.pos
        self.vel = Vector.Normalize(self.vel) * 0.01

        # Deal damage
        self.ammo -= 1
        enemy.injure(self.damage)

        self.attack_timer = self.attack_delay

# Broadcasts a message to all players. Only one of the args have to be set in
# order for the message to be sent. If to_self is set, the message is also
# sent to the sender himself.
def say(self, mtype=None, string=None, entity=None, vector=None, to_self=False):
    if (mtype is not None or
        string is not None or
        entity is not None or
        vector is not None):

        self.has_message = True
        self.message = Message(source=self, mtype=mtype, 
                entity=entity, string=string, vector=vector, to_self=to_self)

# Returns distance from self to the target's position.
def distance_to(self, target):
    return Vector.Distance(self.pos, target.pos)

# Sets the velocity vector, scaled to the given speed, pointing to the target.
# If speed is not given, defaults to self.speed.
def move_to_pos(self, pos, speed=None):
    if speed is None:
        speed = self.speed

    self.vel = Vector.Normalize(pos - self.pos) * speed

def move_from_pos(self, pos, speed=None):
    if speed is None:
        speed = self.speed

    self.vel = Vector.Normalize(self.pos - pos) * speed

def move_to(self, target, speed=None):
    if speed is None:
        speed = self.speed

    self.vel = Vector.Normalize(target.pos - self.pos) * speed

def move_from(self, target, speed=None):
    if speed is None:
        speed = self.speed

    self.vel = Vector.Normalize(self.pos - target.pos) * speed

# Given self and a list of entities, returns the nearest entity and the 
# distance to that entity
def get_nearest(self, entities, with_distance=False):
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
