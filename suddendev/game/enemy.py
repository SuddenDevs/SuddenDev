from .entity import Entity
from .vector import Vector

import random

class Enemy(Entity):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.pos = Vector(random.random() * self.game.map.width,
                            random.random() * self.game.map.height)
        self.speed = self.game.gc.ENEMY_SPEED

        self.range_attackable = self.game.gc.ENEMY_RANGE_ATTACKABLE
        self.damage = self.game.gc.ENEMY_DAMAGE
        self.attack_delay = self.game.gc.ENEMY_ATTACK_DELAY
        self.attack_timer = self.attack_delay
    
    def update(self, delta):
        if self.attack_timer > 0:
            self.attack_timer -= 1

        #Find Nearest Player
        ps = self.game.players
        target = ps[0].pos
        target_player = ps[0]
        mag_min = Vector.Length(self.pos - target)
        for p in ps:
            mag = Vector.Length(self.pos - p.pos)
            if mag < mag_min:
                target = p.pos
                target_player = p
                mag_min = mag

        distance_thresh = 3

        # If health < 50%, run away, otherwise run towards
        if self.health >= self.healthMax / 2:
            # Shoot if possible
            if mag_min <= self.range_attackable and self.attack_timer == 0:
                self.shoot(p)
                return super().update(delta)

            # Prevent spazzing when on top of player
            if mag_min < distance_thresh:
                self.vel = Vector(0,0)
                return super().update(delta)
            to = target - self.pos
        else:
            to = self.pos - target
        mag = Vector.Length(to)

        self.vel = Vector.Normalize(to) * min(mag, self.speed)
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

            self.attack_timer = self.attack_delay
