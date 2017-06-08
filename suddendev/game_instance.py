#!/usr/bin/python3
from .game.game import Game
from .game.state_encoder import StateEncoder, encodeState
from . import socketio
from .game.game_config import GameConfig as gc
import time
import datetime
import time

NAMESPACE = '/game-session'

class GameInstance:
    def __init__(self, game_id, player_names, scripts):
        #TODO: take wave no. as a parameter
        wave = 1
        self.game_id = game_id
        self.start_time = datetime.datetime.now()
        self.game = Game(wave, player_names, scripts)
        self.log = None

        self.update_log(self.game.log)

    def update_log(self, log):
        if log is not None:
            if self.log is None:
                self.log = { 'errors' : [], 'stdout' : [] }

            self.log['errors'] += log['errors']
            self.log['stdout'] += log['stdout']

    #Generator
    def run(self):
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
            log = self.game.tick(gc.FRAME_INTERVAL_SIM)
            self.update_log(log)

            # Display frame sampling
            frame_timer += gc.FRAME_INTERVAL_SIM
            if frame_timer >= gc.FRAME_INTERVAL_DISPLAY:
                frame_timer -= gc.FRAME_INTERVAL_DISPLAY
                state_counter += 1
                batch.append(encodeState(self.game))
                self.game.events_flush()

            if state_counter == gc.BATCHSIZE or not self.game.active:
                #Client Update
                yield batch, self.log
                self.log = None
                batch = []
                state_counter = 0
