#!/bin/bash
source local-envs.sh
sh run-redis.sh &
celery worker -A suddendev.celery --loglevel=info &
python wsgi.py
