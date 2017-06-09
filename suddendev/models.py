import flask_sqlalchemy as flask_sql
import datetime
from flask_login import UserMixin
from .game.game_config import GameConfig as gc

db = flask_sql.SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String(100), unique=True, nullable=False)
    picture = db.Column(db.String, nullable=True)
    script = db.Column(db.String, default=gc.P_DEFAULT_SCRIPT)
    active = db.Column(db.Boolean, default=False)
    tokens = db.Column(db.Text)
