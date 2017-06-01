#/bin/bash
export DATABASE_URL=postgresql:///suddendev_test
export APP_SETTINGS=suddendev.config.TestingConfig
export SECRET_KEY=test_key_pls_ignore
export REDIS_URL=redis://localhost:6379/0
sh run-redis.sh &
venv/bin/celery worker -A suddendev.celery --loglevel=info &
tox
