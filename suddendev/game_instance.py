#!/usr/bin/python3
from .game.game import Game
from .game.state_encoder import StateEncoder, encodeState
from . import socketio
import flask
import flask_socketio as fsio
import datetime

NAMESPACE = '/game-session'

class GameInstance:
    def __init__(self, game_id, app):
        self.app = app
        self.game_id = game_id
        self.start_time = datetime.datetime.now()
        self.game = Game()

    def update_clients(self):
        while True:
            self.game.tick(10)
            #json = encodeState(state)
            json = {"hello" : "noob"}
            with self.app.app_context():
                # fsio.emit('status', json, namespace=NAMESPACE, room=self.game_id)
                fsio.emit('status', json, namespace=NAMESPACE, broadcast=True)

    # join
    # leave
    # def updateClients(self):
