#!/bin/bash
sudo rabbitmq-server -detached
sh run-redis.sh &
heroku local
