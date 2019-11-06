from flask_wtf import FlaskForm, Form
from wtforms import StringField, BooleanField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class RegisterForm:

    def form(registereduser):

        class F(FlaskForm):
            name = StringField('Name', validators=[DataRequired()])
            email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
            password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
            state = StringField('State', validators=[DataRequired()])
            district = IntegerField('District', validators=[DataRequired()])
            submit = SubmitField("Create New Account")
        return F()



class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password', validators=[DataRequired()])