from .entity import Entity
from .vector import Vector
from .game_config import GameConfig as gc
from enum import Enum

class Powerup(Entity):
    def __init__(self, pos, powerup_type):
        super().__init__()
        self.powerup_type = powerup_type
        self.pos = pos
        self.size = gc.POW_SIZE
        self.value = 0

        if self.powerup_type == PowerupType.AMMO_UP:
            self.value = gc.POW_AMMO_UP_VALUE
        elif self.powerup_type == PowerupType.HEALTH_UP:
            self.value = gc.POW_HEALTH_UP_VALUE

    def pickup(self, player):
        if self.powerup_type == PowerupType.AMMO_UP:
            player.ammo += self.value
        elif self.powerup_type == PowerupType.HEALTH_UP:
            player.health = min(self.healthMax, player.health + self.value)

    def intersects(self, player):
        distance = Vector.Distance(self.pos, player.pos)
        radii = self.size + player.size
        return distance <= radii

class PowerupType(Enum):
    AMMO_UP = 'ammo_up'
    HEALTH_UP = 'health_up'
