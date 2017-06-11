#!/usr/bin/python3
from .game.game import Game
from .game.state_encoder import StateEncoder, encodeState
from .game.game_config import GameConfig as gc
import datetime
import time

class GameInstance:
    def __init__(self, game_id, player_names, scripts, wave=1):
        self.game_id = game_id
        self.start_time = datetime.datetime.now()
        self.game = Game(wave, player_names, scripts)

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
            self.game.tick(gc.FRAME_INTERVAL_SIM)

            # Display frame sampling
            frame_timer += gc.FRAME_INTERVAL_SIM
            if frame_timer >= gc.FRAME_INTERVAL_DISPLAY:
                frame_timer -= gc.FRAME_INTERVAL_DISPLAY
                state_counter += 1
                batch.append(encodeState(self.game))
                self.game.events_flush()

            if state_counter == gc.BATCHSIZE or not self.game.active:
                #Client Update
                yield batch
                batch = []
                state_counter = 0

    def was_cleared(self):
        """Returns a boolean indicating whether the wave was cleared, after gameplay."""
        return self.game.was_cleared()
