import flask_sqlalchemy as flask_sql
import datetime


db = flask_sql.SQLAlchemy()


class ChatRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_key = db.Column(db.String, unique=True)
    end_time = db.Column(db.DateTime)

    def __init__(self, room_key):
        self.room_key = room_key
        self.end_time = datetime.datetime.now() + \
                datetime.timedelta(minutes=30)
