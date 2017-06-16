#!/usr/bin/python3.5

from .vector import Vector
from .color import Color3, random_color3
from .player import Player
from .enemy import Enemy
from .pickup import Pickup, PickupType
from .enemy_type import EnemyType
from .wall import Wall
from .core import Core
from .event import Event, EventType, GameOverType
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
    def __init__(self, wave, player_names, scripts, player_ids):
        self.walls = []
        self.events = []
        self.enemies = []
        self.pickups = []

        self.stats = {}

        self.wave = wave
        self.gc = GameConfig(wave)

        self.enemy_spawn_timer = self.gc.ENEMY_SPAWN_DELAY

        self.pickup_spawn_timer = self.gc.POW_SPAWN_DELAY
        self.pickup_count = 0

        self.time = 0
        self.active = True

        #Map
        self.map = Map(self.gc.MAP_WIDTH, self.gc.MAP_HEIGHT)

        #Core
        self.core = Core()
        self.core.pos = Vector(self.map.width/2, self.map.height/2)
        self.core.health_max = self.gc.CORE_HEALTH
        self.core.health = self.core.health_max

        #Players
        self.init_players(player_names, scripts, player_ids)

        self.events_add(Event(EventType.GAME_START))

    def init_players(self, player_names, scripts, player_ids):
        player_count = len(player_names)
        self.players = []
        for i in range(player_count):
            name = player_names[i]
            script = scripts[i]
            player_id = player_ids[i]

            angle = i * 2 * math.pi / player_count - math.pi/2
            player = Player(name, random_color3(), self, script, player_id)
            player.pos = self.get_random_spawn(player.size)
            player.pos = self.core.pos\
                         + Vector(math.cos(angle), math.sin(angle))\
                         * (self.core.size + player.size * 2)
            self.init_player_stats(player_id)
            self.players.append(player)

    def init_player_stats(self, player_id):
        self.stats[player_id] = dict()
        self.stats[player_id]['kills'] = 0

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
        result = self.check_if_game_over()
        if result is not None:
            self.active = False
            self.events_add(Event(EventType.GAME_END, result))

            # TODO: nicer way of seeing if the wave was cleared
            self.cleared = result == GameOverType.WIN

    def check_if_game_over(self):
        if len(self.enemies) == 0 and not self.gc.enemy_types:
            return GameOverType.WIN
        elif self.core.health <= 0:
            return GameOverType.LOSE_CORE
        elif len(self.players) == 0:
            return GameOverType.LOSE_PLAYERS
        elif self.time >= self.gc.TIME_LIMIT:
            return GameOverType.LOSE_TIMEOUT
        else:
            return None

    def update_players(self, delta):
        #Update Players
        for p in self.players:
            if p.health <= 0:
                self.players.remove(p)
                self.events_add(Event(EventType.PLAYER_DEATH, p))
                break

            pos = self.clamp_pos(p.update(delta))
            if not self.collides_with_walls(pos, p.size):
                p.pos = pos

            # Pickup pickups
            for pu in self.pickups:
                if pu.intersects(p):
                    self.events_add(Event(EventType.PICKUP_USED, pu))
                    pu.pickup(p)
                    self.pickups.remove(pu)

    def update_enemies(self, delta):
        #Update Enemies
        for e in self.enemies:
            if e.health <= 0:
                self.enemies.remove(e)
                self.events_add(Event(EventType.ENEMY_DEATH, e))
                if e.is_boss:
                    # TODO make less ugly
                    # Temporarily fake that we're in a lower wave to spawn non-boss enemies
                    temp_gc = self.gc
                    self.gc = GameConfig(self.wave - 1)
                    self.wave -= 1
                    types = [EnemyType.CORE_KILLER, EnemyType.PLAYER_KILLER]
                    for i in range(self.gc.BOSS_MINION_NUM):
                        position = Vector(e.pos.x, e.pos.y)
                        position.x += random.randint(-e.size * 2, e.size * 2)
                        position.y += random.randint(-e.size * 2, e.size * 2)
                        self.gc.enemy_types.append(random.choice(types))
                        e = self.spawn_enemy(position)
                        e.speed_max = 40
                        e.damage = 1
                        e.attack_delay = 15
                        e.size = 5
                        e.health_max = 20
                        e.health = 20
                    self.wave += 1
                    self.gc = temp_gc
                    
            else:
                pos = self.clamp_pos(e.update(delta))
                if not self.collides_with_walls(pos, e.size):
                    e.pos = pos

    def spawn_pickups(self):
        # pickupTypes = [PickupType.AMMO, PickupType.HEALTH]
        pickupTypes = [pickup for _, pickup in PickupType.__members__.items()]

        #Pickup Spawning
        if (self.pickup_spawn_timer <= 0
            and self.pickup_count < self.gc.POW_LIMIT
            and random.random() < self.gc.POW_SPAWN_PROBABILITY):

            pu = Pickup(self.get_random_spawn(self.gc.POW_SIZE), random.choice(pickupTypes))
            self.pickups.append(pu)
            self.pickup_count += 1
            self.events_add(Event(EventType.PICKUP_SPAWN, pu))

    def spawn_enemy(self, position=None):
        enemy_type=random.choice(self.gc.enemy_types)
        self.gc.enemy_types.remove(enemy_type)
        enemy = Enemy(self, enemy_type=enemy_type)
        if position is None:
            enemy.pos = random_pos_edge(enemy.size,
                                        self.map.width, self.map.height)
        else:
            enemy.pos = position
        self.enemies.append(enemy)
        self.events_add(Event(EventType.ENEMY_SPAWN, enemy))
        return enemy

    def spawn_enemies(self):
        #Enemy Spawning
        if (self.enemy_spawn_timer <= 0
            and self.gc.enemy_types
            and random.random() < self.gc.ENEMY_SPAWN_PROBABILITY):
            self.spawn_enemy()

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
    
    def find_by_tag(self, tag):
        for e in self.enemies:
            if e.tag == tag:
                return e
        for e in self.players:
            if e.tag == tag:
                return e
        for e in self.pickups:
            if e.tag == tag:
                return e
        if self.core.tag == tag:
            return self.core
        return None

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

    def get_map_width(self):
        return self.map.width

    def get_map_height(self):
        return self.map.height
