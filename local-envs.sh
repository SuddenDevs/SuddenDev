#!/bin/bash
export DATABASE_URL=postgresql:///suddendev_dev
export APP_SETTINGS=suddendev.config.DevelopmentConfig
export REDIS_URL=redis://localhost:6379/0
export CLOUDAMQP_URL=amqp://guest:guest@localhost:5672//
export LOG_LEVEL=DEBUG
export CLIENT_SECRET=7he9FnNvgC7C68FQZ0uAytr9
export OAUTHLIB_INSECURE_TRANSPORT=1
