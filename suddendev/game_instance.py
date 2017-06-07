#!/usr/bin/python3
from .game.game import Game
from .game.state_encoder import StateEncoder, encodeState
from . import socketio
from .game.game_config import GameConfig
import time
import datetime
import time

NAMESPACE = '/game-session'

class GameInstance:
    def __init__(self, game_id, player_names, scripts):
        self.game_id = game_id
        self.start_time = datetime.datetime.now()
        self.gc = GameConfig(wave=1)
        self.game = Game(self.gc, player_names, scripts)

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
            self.game.tick(self.gc.FRAME_INTERVAL_SIM)

            # Display frame sampling
            frame_timer += self.gc.FRAME_INTERVAL_SIM
            if frame_timer >= self.gc.FRAME_INTERVAL_DISPLAY:
                frame_timer -= self.gc.FRAME_INTERVAL_DISPLAY
                state_counter += 1
                batch.append(encodeState(self.game))

            # if state_counter == batchSize or not self.game.active:
                # #Client Update
                # yield batch 
                # batch = []
                # state_counter = 0
            if not self.game.active:
                return batch
