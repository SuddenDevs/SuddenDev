from . import celery
import time

@celery.task
def run_game_task():
    time.sleep(4)
    return {'status' : 'game is done', 'result' : 'dasf'}
