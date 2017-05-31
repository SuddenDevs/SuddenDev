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
    spawnrate = 0.1
    spawnrate_variance = 0.05

    def __init__(self):
        #Map
        self.map = Map(600, 600)

        #Players
        self.players = []
        for i in range(3):
            player = Player(i, Color3(255, 0, 0))
            self.players.append(player)

        #Metadata
        self.time = 0

    #### Main Loop ####
    def tick(self, delta):
        #Timekeeping
        self.time += delta

        #Update Players
        for p in self.players:
            p.update(delta)
