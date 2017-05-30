from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required


class EnterChatForm(Form):
    """Accepts a key."""
    key = StringField('Key', validators=[Required()])
    submit = SubmitField('Start session.')


class SetupChatForm(Form):
    """Accepts a name."""
    submit = SubmitField('Create session.')
