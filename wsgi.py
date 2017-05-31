"""
WSGI script run on Heroku using gunicorn.
Exposes the app and configures it to use Heroku environment vars.
"""
import os
from suddendev import create_app, socketio

app = create_app()
port = int(os.environ.get("PORT", 5000))
socketio.run(app, host='0.0.0.0', port=port)
