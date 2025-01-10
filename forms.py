from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()], render_kw={'placeholder':'username'})
    password = StringField(validators=[DataRequired()], render_kw={'placeholder':'password'})
    submit = SubmitField()