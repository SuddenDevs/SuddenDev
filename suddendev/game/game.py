#!/usr/bin/python3.5

from .vector import Vector
from .color import Color3, random_color3
from .player import Player
from .enemy import Enemy
from .powerup import Powerup, PowerupType
from .wall import Wall
from .core import Core
from .event import Event, EventType
from .game_config import GameConfig

import time
import random

class Map:
    def __init__(self, width, height):
        random.seed(time.time())
        self.width = width
        self.height = height

class Game:
    walls = []
    events = []
    enemies = []
    powerups = []

    enemy_spawn_timer = 0
    powerup_spawn_timer = 0
    powerup_count = 0

    time = 0
    active = True

    def __init__(self, wave, player_names, scripts):
        self.wave = wave
        self.gc = GameConfig(wave)
        #Map
        self.map = Map(self.gc.MAP_WIDTH, self.gc.MAP_HEIGHT)

        #Core
        self.core = Core()
        self.core.pos = Vector(self.map.width/2, self.map.height/2)

        #Players
        self.init_players(player_names, scripts)

    def init_players(self, player_names, scripts):
        player_count = len(player_names)
        self.players = []
        for i in range(player_count):
            name = player_names[i]
            script = scripts[i]

            player = Player(name, random_color3(), self, script)
            player.pos = self.get_random_spawn(player.size)
            self.players.append(player)

    def events_add(self, event):
        self.events.append(event)

    def events_flush(self):
        del self.events[:]

    #### Main Loop ####
    def tick(self, delta):
        #Timekeeping
        self.time += delta
        self.enemy_spawn_timer += delta
        self.powerup_spawn_timer += delta

        # Update entities
        self.update_players(delta)
        self.update_enemies(delta)

        self.spawn_powerups()
        self.spawn_enemies()

        #Ending Conditions / Wave Conditions
        if self.time >= self.gc.TIME_LIMIT:
            self.active = False
            self.events_add(Event(EventType.GAME_END))

    def update_players(self, delta):
        #Update Players
        for p in self.players:
            pos = self.clamp_pos(p.update(delta))
            if not self.collides_with_walls(pos, p.size):
                p.pos = pos

            # Pickup powerups
            for pu in self.powerups:
                if pu.intersects(p):
                    self.events_add(Event(EventType.POWERUP_USED, pu))
                    pu.pickup(p)
                    self.powerups.remove(pu)

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

    def spawn_powerups(self):
        # powerupTypes = [PowerupType.AMMO_UP, PowerupType.HEALTH_UP]
        powerupTypes = [powerup for _, powerup in PowerupType.__members__.items()]

        #Powerup Spawning
        if (self.powerup_spawn_timer > self.gc.POW_SPAWN_DELAY
            and self.powerup_count < self.gc.POW_LIMIT
            and random.random() < self.gc.POW_SPAWN_PROBABILITY):

            pu = Powerup(self.get_random_spawn(self.gc.POW_SIZE), random.choice(powerupTypes))
            self.powerups.append(pu)
            self.powerup_count += 1
            self.events_add(Event(EventType.POWERUP_SPAWN, pu))

    def spawn_enemies(self):
        #Enemy Spawning
        if (self.enemy_spawn_timer > self.gc.ENEMY_SPAWN_DELAY
            and len(self.enemies) < self.gc.ENEMY_LIMIT
            and random.random() < self.gc.ENEMY_SPAWN_PROBABILITY):

            #Spawn Enemy
            enemy = Enemy(self)
            self.enemies.append(enemy)
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

