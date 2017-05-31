"""
WSGI script run on Heroku using gunicorn.
Exposes the app and configures it to use Heroku environment vars.
"""
from suddendev import create_app, socketio


app = create_app()
socketio.run(app, host='0.0.0.0')
