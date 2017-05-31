#!/usr/bin/python3
from .game.game import Game
from .game.state_encoder import StateEncoder, encodeState
from . import socketio
import flask
import flask_socketio as fsio
import datetime

NAMESPACE = '/game-session'
sample_json="""
{
	"players": [{
		"tag": 0,
		"healthMax": 100,
		"health": 100,
		"ammo": 10,
		"name": "Bob",
		"color": {
			"r": 255,
			"g": 255,
			"b": 255
		},
		"pos": {
			"x": 100,
			"y": 500
		},
		"vel": {
			"x": 100,
			"y": 500
		},
		"size": {
			"x": 100,
			"y": 500
		}
	}],
	"enemies": [{
		"tag": 0,
		"healthMax": 100,
		"health": 100,
		"pos": {
			"x": 100,
			"y": 500
		},
		"vel": {
			"x": 100,
			"y": 500
		},
		"size": {
			"x": 100,
			"y": 500
		}
	}],
	"powerups": [{
		"tag": 0,
		"healthMax": 100,
		"health": 100,
		"pos": {
			"x": 100,
			"y": 500
		},
		"vel": {
			"x": 100,
			"y": 500
		},
		"size": {
			"x": 100,
			"y": 500
		}
	}],
	"core": {
		"tag": 0,
		"healthMax": 100,
		"health": 100,
		"pos": {
			"x": 100,
			"y": 500
		},
		"vel": {
			"x": 100,
			"y": 500
		},
		"size": {
			"x": 100,
			"y": 500
		}
	}
}
"""
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
            json = sample_json
            with self.app.app_context():
                fsio.emit('status', json, namespace=NAMESPACE, room=self.game_id)
                # fsio.emit('status', json, namespace=NAMESPACE, broadcast=True)

    # join
    # leave
    # def updateClients(self):
