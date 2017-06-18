from . import celery
from .game_instance import GameInstance
import time

@celery.task(time_limit=10, max_retries=3)
def play_round(game_id, player_names, scripts, player_ids, colors, wave):
    game = GameInstance(game_id, player_names, scripts, player_ids, colors, wave=wave)
    game_states = []

    for batch in game.run():
        game_states += batch

    # return if the test round was cleared
    return game.was_cleared(), game_states
