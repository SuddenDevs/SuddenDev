from . import celery
from .game_instance import GameInstance
import json

@celery.task
def play_game(game_id, player_names, scripts):
    game = GameInstance(game_id, player_names, scripts)
    return '{\"result\": [ ' + ','.join(game.run()) + ']}'
