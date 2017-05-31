#!/usr/bin/python3.5

from .vector import Vector
from .color import Color3
from .player import Player
from .enemy import Enemy

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

    def __init__(self):
        #Map
        self.map = Map(600, 600)

        #Players
        self.players = []
        for i in range(3):
            player = Player(i, Color3(255, 0, 0))
            self.players.append(player)

        #Enemies
        self.enemies = []
        self.enemy_limit = 5
        self.enemy_spawn_timer = 0

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
        if (self.enemy_spawn_timer > enemy_spawn_delay
            and len(self.enemies) < self.enemy_limit):
            #Spawn Enemy
            enemy = Enemy()
            self.enemies.append(enemy)

        #Powerup Spawning
        
        #Ending Conditions / Wave Conditions
