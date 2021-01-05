from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

class LoginForm(FlaskForm):
    email   = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6,max=15)])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    email   = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=6,max=15)])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(),Length(min=6,max=15), EqualTo('password')])
    submit = SubmitField("Register Now")

class GroupCreation(FlaskForm):
    name = StringField("Group Name", validators=[DataRequired(), Length(min=1, max=100)])
    submit = SubmitField("Register Now")

class JoinGroup(FlaskForm):
    groupID = IntegerField("Group ID", validators = [DataRequired()])
    submit = SubmitField("Join")