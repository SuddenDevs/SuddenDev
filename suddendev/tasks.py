from . import celery
from .game_instance import GameInstance
from .config import Config
import json
import flask_socketio as fsio

@celery.task
def play_game(game_id, player_names, scripts, namespace):
    game = GameInstance(game_id, player_names, scripts)
    socketio = fsio.SocketIO(message_queue=Config.REDIS_URL)

    for batch, errors in game.run():
        for e in errors:
            socketio.emit('message', '[ERROR] ' + e, namespace=namespace)

        socketio.emit('result', '{\"result\": [ ' + ','.join(batch) + ']}', room=game_id, namespace=namespace)
