from .vector import Vector
import sys

# Returns a velocity vector, scaled to the given speed, pointing to the target.
# If speed is not given, defaults to self.speed.
def move_to(self, target, speed=None):
    if speed is None:
        speed = self.speed

    return Vector.Normalize(target - self.pos) * speed

# Returns a velocity vector, scaled to the given speed, pointing away from the target.
# If speed is not given, defaults to self.speed.
def move_from(self, target, speed=None):
    if speed is None:
        speed = self.speed

    return Vector.Normalize(self.pos - target) * speed

# Given self and a list of entities, returns the nearest entity and the 
# distance to that entity
def get_nearest(self, entities):
    nearest_distance = sys.maxsize
    nearest = None

    for e in entities:
        distance = Vector.Distance(self.pos, e.pos)
        if distance < nearest_distance:
            neareast = e
            nearest_distance = distance

    return nearest, nearest_distance
