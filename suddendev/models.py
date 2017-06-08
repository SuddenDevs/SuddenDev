import flask_sqlalchemy as flask_sql
import datetime
from flask_login import UserMixin

db = flask_sql.SQLAlchemy()

DEFAULT_SCRIPT = """
# Attacking script
timer = 0

def update(player, delta):
    global timer
    timer += delta
	
    # Find Target
    min_dist = sys.float_info.max
    target = None
    for e in enemies_visible:
        mag = Vector.Length(e.pos - player.pos)
        if mag < min_dist:
            min_dist = mag
            target = e
			
    if target is not None:
        diff = player.pos - target.pos
        mag = min(player.speed, min_dist)
        player.vel = Vector.Normalize(diff) * mag
    else:
        player.vel = Vector(0,0)
"""

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String(100), unique=True, nullable=False)
    picture = db.Column(db.String, nullable=True)
    script = db.Column(db.String, default=DEFAULT_SCRIPT)
    active = db.Column(db.Boolean, default=False)
    tokens = db.Column(db.Text)
