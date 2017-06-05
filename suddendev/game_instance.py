#!/usr/bin/python3
from .game.game import Game
from .game.state_encoder import StateEncoder, encodeState
from . import socketio
import time
import flask
import flask_socketio as fsio
import datetime
import time

NAMESPACE = '/game-session'

# Currently Unused
framerate = 30
interval = 1/framerate

# Packet size in number of game states
batchSize = 500

class GameInstance:
    def __init__(self, game_id, player_names, scripts):
        self.game_id = game_id
        self.start_time = datetime.datetime.now()
        self.game = Game(player_names, scripts)
        self.state_counter = 0
    
    #Generator
    def run(self):
        time_last = time.time()
        batch = []

        #Main Loop
        while self.game.active:
            #Timekeeping
            time_current = time.time()
            delta = time_current - time_last
            time_last = time_current

            #Gameplay Update
            self.game.tick(0.1)
            batch.append(encodeState(self.game))
            self.state_counter += 1
            
            if self.state_counter == batchSize or not self.game.active:
                #Client Update
                yield batch 
                batch = []
                self.state_counter = 0
