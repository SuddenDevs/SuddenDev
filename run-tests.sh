#/bin/bash
sh run-redis.sh &
venv/bin/celery worker -A suddendev.celery --loglevel=info &
tox
