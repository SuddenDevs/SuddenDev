"""
WSGI script run on Heroku using gunicorn.
Exposes the app and configures it to use Heroku environment vars.
"""
import os
from suddendev import create_app, socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app)
