from . import celery, celery_socketio
from .game_instance import GameInstance

@celery.task
def play_game(game_id, player_names, scripts, namespace, room, wave=1):
    game = GameInstance(game_id, player_names, scripts, wave=wave)

    final_result = None
    for batch, game_result in game.run():
        celery_socketio.emit('result', '{\"result\": [ ' + ','.join(batch) + ']}', room=room, namespace=namespace)

        final_result = game_result

    return final_result
