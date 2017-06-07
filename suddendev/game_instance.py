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

# Game steps per second
# simulation rate >= display rate
framerate_sim = 30
framerate_display = 15

frame_interval_sim = 1/framerate_sim
frame_interval_display = 1/framerate_display

# Packet size in number of game states
batchSize = 500

class GameInstance:
    def __init__(self, game_id, player_names, scripts):
        self.game_id = game_id
        self.start_time = datetime.datetime.now()
        self.game = Game(player_names, scripts)

    #Generator
    def run(self):
        global batchSize
        global frame_interval_sim
        global frame_interval_display

        time_last = time.time()
        batch = []
        frame_timer = 0
        state_counter = 0

        #Main Loop
        while self.game.active:
            #Timekeeping
            time_current = time.time()
            delta = time_current - time_last
            time_last = time_current

            #Gameplay Update
            self.game.tick(frame_interval_sim)

            # Display frame sampling
            frame_timer += frame_interval_sim
            if frame_timer >= frame_interval_display:
                frame_timer -= frame_interval_display
                state_counter += 1
                batch.append(encodeState(self.game))

            # if state_counter == batchSize or not self.game.active:
                # #Client Update
                # yield batch 
                # batch = []
                # state_counter = 0
            if not self.game.active:
                return batch
