#!/bin/bash
export SECRET_KEY=fake_secret_key_for_local_deployment
export DATABASE_URL=postgresql:///suddendev_dev
export APP_SETTINGS=suddendev.config.DevelopmentConfig
export LOG_LEVEL=DEBUG
