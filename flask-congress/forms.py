from flask_wtf import FlaskForm, Form
from wtforms import StringField, BooleanField, IntegerField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class RegisterForm:

    def form(lstStates):

        class F(FlaskForm):
            name = StringField('Name', validators=[DataRequired()])
            email = StringField('Email', validators=[DataRequired(), Email()])
            password = PasswordField('Password', validators=[DataRequired()])
            state = SelectField('State', choices = lstStates)
            district = IntegerField('District', validators=[DataRequired()])
            submit = SubmitField("Create New Account")
        return F()



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Login")


class UpdateForm():
    def form(lstStates):
        class F(FlaskForm):
            name = StringField('Name', validators = [])
            password = PasswordField('Password', validators = [])
            state = SelectField('State', choices = lstStates)
            district = IntegerField('District', validators = [])
            submit = SubmitField('Submit')
        return F()