from . import celery, celery_socketio
from .game_instance import GameInstance

@celery.task
def play_game(game_id, player_names, scripts, namespace, room):
    game = GameInstance(game_id, player_names, scripts)

    for batch in game.run():
        celery_socketio.emit('result', '{\"result\": [ ' + ','.join(batch) + ']}', room=room, namespace=namespace)
