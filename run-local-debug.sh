#!/bin/bash
source local-envs.sh
sh run-redis.sh &
sudo rabbitmq-server -detached
celery worker -A suddendev.celery --loglevel=info &
python wsgi.py
