from . import celery
from .game_instance import GameInstance
import time
import json

@celery.task
def play_game(game_id, player_names):
    game = GameInstance(game_id, player_names)
    return '{\"result\": [ ' + ','.join(game.run()) + ']}'
