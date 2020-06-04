from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, EqualTo,\
    Optional, Email, EqualTo


class SignUpForm(FlaskForm):
    firstname = StringField('firstname',validators=[InputRequired()])
    lastname = StringField('lastname',validators=[InputRequired()])
    username = StringField('username', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired(), Length(min=6),
     Email(message='Enter a vaild Email')])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6)])
    confirm = PasswordField('Confirm your password',validators=[InputRequired(), EqualTo('password',
    message='Passwords must match')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    """User Login Form."""
    username= StringField('username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Log In')

class FeedbackForm(FlaskForm):
    """Feedbacks Form."""
    title = StringField('title', validators=[InputRequired(), Length(min=1)])
    feedback = TextAreaField('feedback', validators=[InputRequired(), Length(min=1)])
    submit = SubmitField('Submit')
