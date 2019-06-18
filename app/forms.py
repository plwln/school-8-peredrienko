from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length

class PostForm(FlaskForm):
    title = TextAreaField('Заголовок', validators=[
        DataRequired(), Length(min=1, max=140)])
    description = TextAreaField('Описание', validators=[
        DataRequired(), Length(min=1, max=140)])
    post = TextAreaField('Текст', validators=[
        DataRequired(), Length(min=1)])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')