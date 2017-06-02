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

class GameInstance:
    def __init__(self, game_id, player_names):
        self.game_id = game_id
        self.start_time = datetime.datetime.now()
        self.game = Game(player_names)
        self.states = []
    
    def run(self):
        time_last = time.time()

        #Main Loop
        for i in range(1000):
            #Timekeeping
            time_current = time.time()
            delta = time_current - time_last
            time_last = time_current
            #time.sleep(100/1000)

            #Gameplay Update
            self.game.tick(0.5)

            #Client Update
            self.states.append(encodeState(self.game))

        return self.states
