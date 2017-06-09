web: gunicorn -w 1 --worker-class eventlet wsgi:app --log-file=- --bind 0.0.0.0:$PORT
worker: celery -c 1 worker -A suddendev.celery --loglevel=info
