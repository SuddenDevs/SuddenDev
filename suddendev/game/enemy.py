from .entity import Entity
from .enemy_type import EnemyType
from .vector import Vector
from .event import Event, EventType
from .util import *

import random

class Enemy(Entity):
    def __init__(self, game, enemy_type=EnemyType.DEFAULT):
        super().__init__()
        self.game = game
        self.pos = Vector(0,0)
        self.speed = self.game.gc.ENEMY_SPEED

        self.range_visible = self.game.gc.ENEMY_RANGE_VISIBLE
        self.range_attackable = self.game.gc.ENEMY_RANGE_ATTACKABLE
        self.damage = self.game.gc.ENEMY_DAMAGE
        self.attack_delay = self.game.gc.ENEMY_ATTACK_DELAY
        self.attack_timer = 0
        self.size = self.game.gc.ENEMY_SIZE
        self.healthMax = self.game.gc.ENEMY_HEALTH
        self.health = self.healthMax
        self.enemy_type=enemy_type

        self.is_boss = self.game.wave % self.game.gc.BOSS_WAVE_MULTIPLES == 0
    
    def update(self, delta):
        if self.attack_timer > 0:
            self.attack_timer -= 1

        if self.enemy_type == EnemyType.DEFAULT:
            return self.update_default(delta)
        elif self.enemy_type == EnemyType.BOSS:
            return self.update_default(delta)
        elif self.enemy_type == EnemyType.CORE_KILLER:
            return self.update_core_killer(delta)
        elif self.enemy_type == EnemyType.PLAYER_KILLER:
            return self.update_player_killer(delta)

    def update_default(self, delta):
        players = []

        # Everyone's already dead
        if len(self.game.players) == 0:
            return super().update(delta)

        # for p in self.game.players:
            # if distance_to(self, p) <= self.range_visible:
                # players.append(p)

        if len(players) == 0:
            if distance_to(self, self.game.core) > self.range_attackable:
                move_to(self, self.game.core)

            enemy_shoot(self, self.game.core)

            return super().update(delta)

        # Find nearest player
        nearest_player, distance = get_nearest(self, players, True)

        # If health < 50%, run away, otherwise run towards
        # Bosses never run from anyone
        if self.is_boss or self.health >= self.healthMax / 2:
            if distance > self.range_attackable:
                move_to(self, nearest_player)

            enemy_shoot(self, nearest_player)
        else:
            move_from(self, nearest_player)

        return super().update(delta)

    def update_core_killer(self, delta):
        # Go to core and start attacking
        if distance_to(self, self.game.core) > self.range_attackable:
            move_to(self, self.game.core)

        enemy_shoot(self, self.game.core)

        return super().update(delta)

    def update_player_killer(self, delta):
        players = self.game.players

        if len(players) == 0:
            return super().update(delta)

        # Find nearest player
        nearest_player, distance = get_nearest(self, players, True)

        # Go towards him and start shooting
        move_to(self, nearest_player)
        enemy_shoot(self, nearest_player)

        return super().update(delta)
