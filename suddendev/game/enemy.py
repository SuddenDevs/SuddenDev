from .entity import Entity
from .vector import Vector
from .event import Event, EventType
from .util import *

import random

class Enemy(Entity):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.pos = Vector(random.random() * self.game.map.width,
                            random.random() * self.game.map.height)
        self.speed = self.game.gc.ENEMY_SPEED

        self.range_visible = self.game.gc.ENEMY_RANGE_VISIBLE
        self.range_attackable = self.game.gc.ENEMY_RANGE_ATTACKABLE
        self.damage = self.game.gc.ENEMY_DAMAGE
        self.attack_delay = self.game.gc.ENEMY_ATTACK_DELAY
        self.attack_timer = self.attack_delay
    
    def update(self, delta):
        if self.attack_timer > 0:
            self.attack_timer -= 1

        players = []

        # Everyone's already dead
        if len(self.game.players) == 0:
            return super().update(delta)

        for p in self.game.players:
            if distance_to(self, p) <= self.range_visible:
                players.append(p)

        if len(players) == 0:
            if distance_to(self, self.game.core) > self.range_attackable:
                move_to(self, self.game.core)

            if distance_to(self, self.game.core) <= self.range_attackable:
                enemy_shoot(self, self.game.core)
                return super().update(delta)

        # Find nearest player
        nearest_player, distance = get_nearest(self, players, True)

        # If health < 50%, run away, otherwise run towards
        if self.health >= self.healthMax / 2:
            if distance <= self.range_attackable:
                move_to(self, nearest_player)

            # Shoot if possible
            if distance <= self.range_attackable and self.attack_timer == 0:
                enemy_shoot(self, nearest_player)
                return super().update(delta)
        else:
            move_from(self, nearest_player)

        return super().update(delta)

    #TODO duplication with player.shoot()
    def shoot(self, enemy):
        if (Vector.Distance(enemy.pos, self.pos) <= self.range_attackable
                and self.attack_timer == 0):
            # Point towards the target
            self.vel = enemy.pos - self.pos
            self.vel = Vector.Normalize(self.vel) * 0.01

            # Deal damage
            enemy.injure(self.damage)

            # Cool down
            self.attack_timer = self.attack_delay

            # Add event
            self.game.events_add(Event(EventType.ATTACK, self, enemy))
