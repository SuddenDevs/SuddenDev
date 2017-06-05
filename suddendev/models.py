import flask_sqlalchemy as flask_sql
import datetime
from flask_login import UserMixin

db = flask_sql.SQLAlchemy()

class GameSetup(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String, unique=True)
    player_count = db.Column(db.Integer)
    start_time = db.Column(db.DateTime)

    def __init__(self, game_id):
        self.game_id = game_id
        self.start_time = datetime.datetime.now()
        self.player_count = 0

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True)
    tokens = db.Column(db.Text)
