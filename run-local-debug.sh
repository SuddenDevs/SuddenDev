#!/bin/bash
source setup-local-flask-env.sh
sh run-redis.sh &
celery worker -A suddendev.celery --loglevel=info &
python wsgi.py