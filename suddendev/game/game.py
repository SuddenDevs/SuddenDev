#!/usr/bin/python3.5

from .vector import Vector
from .color import Color3
from .player import Player
from .enemy import Enemy
from .core import Core

import time
import random

class Map:
    def __init__(self, width, height):
        random.seed(time.time())
        self.width = width
        self.height = height

class Game:
    #### Config ####
    #Enemy Spawning
    enemy_spawn_delay = 1

    def __init__(self, player_names):
        #Map
        self.map = Map(600, 600)

        script = """
something = 1
someparam = 2

def update(self, delta):
    self.vel = Vector(1,1)
                """

        #Players
        self.players = []
        for i in range(4):
            player = Player(player_names[i], Color3(255, 0, 0), self, script)
            player.pos = Vector(random.random()*self.map.width,
                                random.random()*self.map.height)
            self.players.append(player)

        #Enemies
        self.enemies = []
        self.enemy_limit = 5
        self.enemy_spawn_timer = 0

        #Powerups
        self.powerups = []

        #Core
        self.core = Core()
        self.core.pos = Vector(self.map.width/2, self.map.height/2)

        #Metadata
        self.time = 0

    #### Main Loop ####
    def tick(self, delta):
        #Timekeeping
        self.time += delta
        self.enemy_spawn_timer += delta

        #Update Players
        for p in self.players:
            p.update(delta)

        #Update Enemies
        for e in self.enemies:
            e.update(delta)

        #Enemy Spawning
        if (self.enemy_spawn_timer > self.enemy_spawn_delay
            and len(self.enemies) < self.enemy_limit):
            #Spawn Enemy
            enemy = Enemy(self)
            self.enemies.append(enemy)

        #Powerup Spawning
        
        #Ending Conditions / Wave Conditions
