#!/usr/bin/python3.5

from .vector import Vector
from .color import Color3, random_color3
from .player import Player
from .enemy import Enemy
from .wall import Wall
from .core import Core
from .game_config import GameConfig as gc

import time
import random

class Map:
    def __init__(self, width, height):
        random.seed(time.time())
        self.width = width
        self.height = height

class Game:
    def __init__(self, player_names, scripts):
        #Map
        self.map = Map(gc.MAP_WIDTH, gc.MAP_HEIGHT)

        #Events
        self.events = []

        #Core
        self.core = Core()
        self.core.pos = Vector(self.map.width/2, self.map.height/2)

        #Enemies
        self.enemies = []
        self.enemy_limit = gc.ENEMY_LIMIT
        self.enemy_spawn_timer = 0

        #Walls
        self.walls = []

        colors = [
            random_color3(),
            random_color3(),
            random_color3(),
            random_color3()
        ]

        #Players
        self.players = []
        for i in range(gc.PLAYER_COUNT):
            name = player_names[i]
            script = None
            if name in scripts:
                script = scripts[name]

            player = Player(name, colors[i], self, script)
            player.pos = self.get_random_spawn(player.size)
            self.players.append(player)

        #Powerups
        self.powerups = []

        #Metadata
        self.time = 0
        self.active = True

    #### Main Loop ####
    def tick(self, delta):
        #Timekeeping
        self.time += delta
        self.enemy_spawn_timer += delta

        #Update Players
        for p in self.players:
            pos = self.clamp_pos(p.update(delta))
            if not self.collides_with_walls(pos, p.size):
                p.pos = pos

        #Update Enemies
        for e in self.enemies:
            if e.health <= 0:
                self.enemies.remove(e)
            else:
                pos = self.clamp_pos(e.update(delta))
                if not self.collides_with_walls(pos, e.size):
                    e.pos = pos

        #Enemy Spawning
        if (self.enemy_spawn_timer > gc.ENEMY_SPAWN_DELAY
            and len(self.enemies) < self.enemy_limit):
            #Spawn Enemy
            enemy = Enemy(self)
            self.enemies.append(enemy)

        #Powerup Spawning

        #Ending Conditions / Wave Conditions
        if self.time >= 10:
            self.active = False

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

