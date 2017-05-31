import sqlalchemy
import heroku_config
from suddendev import create_app
from suddendev.models import db, ChatRoom
from flask_sqlalchemy import SQLAlchemy


if __name__=='__main__':
    app = create_app(heroku_config.__file__)

    # create an app context
    ctx = app.app_context()
    ctx.push()

    db.drop_all()
    db.create_all()

    ctx.pop()
