#!/usr/bin/python3

import json
from state_encoder import StateEncoder

class Vector:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

class Core:
    health = 50
    position = Vector(10,10)
    
class Player:
    def __init__(self, name, health, tag, ammo, position):
        self.health = health
        self.tag = tag
        self.ammo = ammo
        self.name = name
        self.position = position

class State:
    players = [Player("Bob", 50, 0, 10000, Vector(80,90))]
    enemies = []
    powerups = []
    core = Core()

def main():
    state = State()
    print(json.dumps(state, cls=StateEncoder))

if __name__ == "__main__":
    main()
