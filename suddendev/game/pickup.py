from .entity import Entity
from .vector import Vector
from .game_config import GameConfig as gc
from enum import Enum

class Pickup(Entity):
    def __init__(self, pos, pickup_type):
        super().__init__()
        self.pickup_type = pickup_type
        self.pos = pos
        self.size = gc.POW_SIZE
        self.value = 0

        if self.pickup_type == PickupType.AMMO_UP:
            self.value = gc.POW_AMMO_UP_VALUE
        elif self.pickup_type == PickupType.HEALTH_UP:
            self.value = gc.POW_HEALTH_UP_VALUE

    def pickup(self, player):
        if self.pickup_type == PickupType.AMMO_UP:
            player.ammo += self.value
        elif self.pickup_type == PickupType.HEALTH_UP:
            player.health = min(self.healthMax, player.health + self.value)

    def intersects(self, player):
        distance = Vector.Distance(self.pos, player.pos)
        radii = self.size + player.size
        return distance <= radii

class PickupType(Enum):
    AMMO_UP = 'ammo'
    HEALTH_UP = 'health'
