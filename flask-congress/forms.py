from flask_wtf import FlaskForm, Form
from wtforms import StringField, BooleanField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class RegisterForm:

    def form():

        class F(FlaskForm):
            name = StringField('Name', validators=[DataRequired()])
            email = StringField('Email', validators=[DataRequired(), Email()])
            password = PasswordField('Password', validators=[DataRequired()])
            state = StringField('State', validators=[DataRequired()])
            district = IntegerField('District', validators=[DataRequired()])
            submit = SubmitField("Create New Account")
        return F()



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Login")