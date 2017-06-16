#!/bin/bash
sudo sh run-redis.sh &
sudo rabbitmq-server -detached
heroku local
