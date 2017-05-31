"""
WSGI script run on Heroku using gunicorn.
Exposes the app and configures it to use Heroku environment vars.
"""
import heroku_config
from suddendev import create_app, socketio


app = create_app(heroku_config.__file__)
socketio.run(app, host='0.0.0.0')
