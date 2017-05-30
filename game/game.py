#/usr/bin/python3.5

from vector import Vector
import time

class Entity:
    def __init__(self):
        self.tag = 0
        self.pos = Vector(0, 0)
        self.size = Vector(10, 10)
        self.healthMax = 100
        self.health = self.healthMax

class Player(Entity):
    def __init__(self, name, color):
        self.name = name
        self.color = color
        super().__init__()

class Enemy(Entity):
    def __init__(self):
        super().__init__(self)

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Game:
    #Enemy Spawning
    spawnrate = 0.1
    spawnrate_variance = 0.05

    def __init__(self):
        #Map
        self.map = Map(600, 600)

        #Players
        self.players = []
        for i in range(3):
            player = Player('nameless', 'colorless') 
            self.players.append(player)

        #Metadata
        self.time = 0

    def tick(self, delta):
        #Timekeeping
        self.time += delta

#New Game
game = Game()

#Game Loop
time_last = time.time()
second_timer = 0
frame_counter = 0
while True:
    time_current = time.time()
    delta = time_current - time_last
    time_last = time_current
    second_timer += delta
    frame_counter += 1
    if second_timer > 1:
        print(frame_counter)
        frame_counter = 0
        second_timer = 0
    game.tick(delta)
