from . import celery, celery_socketio
from .game_instance import GameInstance
import time

@celery.task
def play_game(game_id, player_names, scripts, player_ids, namespace, room, wave=1):

    cleared = True
    current_wave = wave - 1
    while cleared:
        current_wave += 1
        game = GameInstance(game_id, player_names, scripts, player_ids, wave=current_wave)
        for batch in game.run():
            celery_socketio.emit('result', '{\"result\": [ ' + ','.join(batch) + ']}', room=room, namespace=namespace)
        cleared = game.was_cleared()

    # return highest reached wave
    return current_wave - 1

@celery.task
def test_round(game_id, player_names, scripts, player_ids, namespace, room, wave=1):
    game = GameInstance(game_id, player_names, scripts, player_ids, wave=wave)
    for batch in game.run():
        celery_socketio.emit('result', '{\"result\": [ ' + ','.join(batch) + ']}', room=room, namespace=namespace)

    # return if the test round was cleared
    return game.was_cleared()
