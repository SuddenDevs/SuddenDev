from . import celery
from .game_instance import GameInstance
import time
import json

@celery.task
def play_game(game_id):
    game = GameInstance(game_id)
    return '{\"result\": [ ' + ','.join(game.run()) + ']}'
