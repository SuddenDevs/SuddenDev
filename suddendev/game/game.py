#!/usr/bin/python3.5

from .vector import Vector
from .color import Color3, random_color3
from .player import Player
from .enemy import Enemy
from .pickup import Pickup, PickupType
from .wall import Wall
from .core import Core
from .event import Event, EventType
from .game_config import GameConfig

import time
import random
import math


def random_pos_edge(size, width, height):
    n = random.getrandbits(2)
    pos = Vector(0, 0)
    r = random.random()
    if n == 0:
        pos = Vector(-size, r * height)
    elif n == 1:
        pos = Vector(width + size, r * height)
    elif n == 2:
        pos = Vector(r * width, -size)
    else:
        pos = Vector(r * width, height + size)
    return pos


class Map:
    def __init__(self, width, height):
        random.seed(time.time())
        self.width = width
        self.height = height

class Game:
    def __init__(self, wave, player_names, scripts):
        self.walls = []
        self.events = []
        self.enemies = []
        self.pickups = []

        self.wave = wave
        self.gc = GameConfig(wave)

        self.enemy_spawn_timer = self.gc.ENEMY_SPAWN_DELAY
        self.enemy_count = 0

        self.pickup_spawn_timer = self.gc.POW_SPAWN_DELAY
        self.pickup_count = 0

        self.time = 0
        self.active = True

        self.game_result = None

        #Map
        self.map = Map(self.gc.MAP_WIDTH, self.gc.MAP_HEIGHT)

        #Core
        self.core = Core()
        self.core.pos = Vector(self.map.width/2, self.map.height/2)
        self.core.healthMax = self.gc.CORE_HEALTH
        self.core.health = self.core.healthMax

        #Players
        self.init_players(player_names, scripts)

        self.events_add(Event(EventType.GAME_START))

    def init_players(self, player_names, scripts):
        player_count = len(player_names)
        self.players = []
        for i in range(player_count):
            name = player_names[i]
            script = scripts[i]

            angle = i * 2 * math.pi / player_count - math.pi/2
            player = Player(name, random_color3(), self, script)
            player.pos = self.get_random_spawn(player.size)
            player.pos = self.core.pos\
                         + Vector(math.cos(angle), math.sin(angle))\
                         * (self.core.size + player.size)
            self.players.append(player)

    def events_add(self, event):
        self.events.append(event)

    def events_flush(self):
        del self.events[:]

    #### Main Loop ####
    def tick(self, delta):
        #Timekeeping
        self.time += delta
        self.enemy_spawn_timer -= delta
        self.pickup_spawn_timer -= delta

        # Update entities
        self.update_players(delta)
        self.update_enemies(delta)

        self.spawn_pickups()
        self.spawn_enemies()

        #Ending Conditions / Wave Conditions
        result, game_result = self.check_if_game_over()
        if result is not None:
            self.active = False
            self.game_result = game_result
            self.events_add(Event(EventType.GAME_END, result))

            # TODO: nicer way of seeing if the wave was cleared
            self.cleared = 'Wave' in result

    def check_if_game_over(self):
        if len(self.enemies) == 0 and self.enemy_count >= self.gc.ENEMY_LIMIT:
            return 'Wave ' + str(self.wave) + ' cleared!', True
        elif len(self.players) == 0 or self.core.health <= 0:
            return 'Game Over', False
        elif self.time >= self.gc.TIME_LIMIT:
            return 'Time limit reached!', False
        else:
            return None, None

    def update_players(self, delta):
        #Update Players
        for p in self.players:
            if p.health <= 0:
                self.players.remove(p)
                self.events_add(Event(EventType.PLAYER_DEATH, p))

            pos = self.clamp_pos(p.update(delta))
            if not self.collides_with_walls(pos, p.size):
                p.pos = pos

            # Pickup pickups
            for pu in self.pickups:
                if pu.intersects(p):
                    self.events_add(Event(EventType.POWERUP_USED, pu))
                    pu.pickup(p)
                    self.pickups.remove(pu)

    def update_enemies(self, delta):
        #Update Enemies
        for e in self.enemies:
            if e.health <= 0:
                self.enemies.remove(e)
                self.events_add(Event(EventType.ENEMY_DEATH, e))
            else:
                pos = self.clamp_pos(e.update(delta))
                if not self.collides_with_walls(pos, e.size):
                    e.pos = pos

    def spawn_pickups(self):
        # pickupTypes = [PickupType.AMMO_UP, PickupType.HEALTH_UP]
        pickupTypes = [pickup for _, pickup in PickupType.__members__.items()]

        #Pickup Spawning
        if (self.pickup_spawn_timer <= 0
            and self.pickup_count < self.gc.POW_LIMIT
            and random.random() < self.gc.POW_SPAWN_PROBABILITY):

            pu = Pickup(self.get_random_spawn(self.gc.POW_SIZE), random.choice(pickupTypes))
            self.pickups.append(pu)
            self.pickup_count += 1
            self.events_add(Event(EventType.POWERUP_SPAWN, pu))

    def spawn_enemies(self):
        #Enemy Spawning
        if (self.enemy_spawn_timer <= 0
            and self.enemy_count < self.gc.ENEMY_LIMIT
            and random.random() < self.gc.ENEMY_SPAWN_PROBABILITY):

            #Spawn Enemy
            enemy = Enemy(self)
            enemy.pos = random_pos_edge(enemy.size,
                                        self.map.width, self.map.height)
            self.enemies.append(enemy)
            self.enemy_count += 1
            self.events_add(Event(EventType.ENEMY_SPAWN, enemy))

    def clamp_pos(self, pos):
        if pos.x < 0:
            pos.x = 0
        if pos.y < 0:
            pos.y = 0
        if pos.x > self.map.width:
            pos.x = self.map.width
        if pos.y > self.map.height:
            pos.y = self.map.height
        return pos

    def collides_with_walls(self, center, size):
        for w in self.walls:
            if w.intersects(center, size):
                return True
        return False

    def get_random_spawn(self, size):
        """ Generates a random position that does not collide with any walls. """
        cond = True
        while cond:
            pos = Vector(random.random()*self.map.width,
                                random.random()*self.map.height)
            cond = self.collides_with_walls(pos, size)
        return pos

    def was_cleared(self):
        return self.cleared

