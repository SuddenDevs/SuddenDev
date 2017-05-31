#!/usr/bin/python3.5

from vector import Vector
from color import Color3
from player import Player
from enemy import Enemy
from game_state import GameState
from core import Core

import time
import random

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def centre(self):
        return Vector(self.width/2, self.height/2)

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
            player = Player(i, Color3(255, 0, 0), self)
            player.pos = Vector(random.random()*self.map.width,
                                random.random()*self.map.height)
            self.players.append(player)

        #Enemies
        self.enemies = []

        #Powerups
        self.powerups = []

        #Core
        self.core = Core(self.map.centre())

        #Metadata
        self.time = 0

        #State
        self.state = GameState(self.players,
                                self.enemies,
                                self.powerups,
                                self.core)

    #### Main Loop ####
    def tick(self, delta):
        #Timekeeping
        self.time += delta

        #Update Players
        for p in game.players:
            p.update(delta)

        #Update Enemies
        for e in game.enemies:
            e.update(delta)

#Setup New Game
random.seed(time.time())
game = Game()

#Game Loop
time_last = time.time()
second_timer = 0
frame_counter = 0
frame_rate = 0
while True:
    time_current = time.time()
    delta = time_current - time_last
    time_last = time_current
    second_timer += delta
    frame_counter += 1
    if second_timer > 1:
        frame_rate = frame_counter
        frame_counter = 0
        second_timer = 0
        print((" ").join(map(str, game.players)))
    game.tick(delta)
