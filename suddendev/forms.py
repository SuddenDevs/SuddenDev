from flask_wtf import Form
from wtforms.fields import SubmitField

class CreateGameForm(Form):
    submit = SubmitField('Create game.')
