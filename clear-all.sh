#!/bin/bash
./run-redis.sh&
sleep .5
source local-envs.sh
python clear-redis.py
python clear-db.py
pkill celery
sudo pkill redis
sleep .5
echo "everything is cleared now yw"
