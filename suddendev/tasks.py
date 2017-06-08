from . import celery
from .game_instance import GameInstance
from .config import Config
import json
import flask_socketio as fsio

@celery.task
def play_game(game_id, player_names, scripts, namespace):
    game = GameInstance(game_id, player_names, scripts)
    socketio = fsio.SocketIO(message_queue=Config.REDIS_URL)

    for batch, log in game.run():
        if log is not None:
            for e in log['errors']:
                socketio.emit('message', '[ERROR] ' + e, namespace=namespace)
            for e in log['stdout']:
                socketio.emit('message', '[OUT] ' + e, namespace=namespace)

        socketio.emit('result', '{\"result\": [ ' + ','.join(batch) + ']}', room=game_id, namespace=namespace)
