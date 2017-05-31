import flask_sqlalchemy as flask_sql
import datetime

db = flask_sql.SQLAlchemy()

class GameController(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String, unique=True)
    start_time = db.Column(db.DateTime)

    def __init__(self, game_id):
        self.game_id = game_id
        self.start_time = datetime.datetime.now()
