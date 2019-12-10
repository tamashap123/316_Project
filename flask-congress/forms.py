from flask_wtf import FlaskForm, Form
from wtforms import StringField, BooleanField, IntegerField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo, Email

class RegisterForm:

    def form(lstStates):

        class F(FlaskForm):
            name = StringField('Name', validators=[DataRequired()])
            email = StringField('Email', validators=[DataRequired(), Email()])
            password = PasswordField('Password', validators=[DataRequired()])
            state = SelectField('State/Territory', choices = lstStates)
            district = IntegerField('District', validators=[InputRequired()])
            submit = SubmitField("Create New Account")
        return F()



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Login")


class UpdateForm():
    def form(lstStates, paststate):
        class F(FlaskForm):
            name = StringField('Name', validators = [])
            password = PasswordField('Password', validators = [])
            state = SelectField('State/Territory', choices = lstStates, default = paststate)
            district = IntegerField('District', validators = [])
            submit = SubmitField('Submit')
        return F()

class CongressmanCompareForm():
    def form(lst):
        class F(FlaskForm):
            congressperson = SelectField('Congressperson', choices = lst)
            submit = SubmitField('Submit')
        return F()

class CongressmanSearchForm():
    def form(lst):
        class F(FlaskForm):
            category = SelectField('Search Category', choices = lst)
            submit = SubmitField('Submit')
        return F()


class CongressmanSearchNameForm():
    def form():
        class F(FlaskForm):
            name = StringField('Name', validators=[DataRequired()])
            submit = SubmitField('Submit')
        return F()


class CongressmanSearchStateTerritoryDistrictForm():
    def form(lst):
        class F(FlaskForm):
            state = SelectField('State/Territory', choices = lst)
            district = IntegerField('District', validators = [])
            submit = SubmitField('Submit')
        return F()

class CongressmanSearchPartyForm():
    def form(lst):
        class F(FlaskForm):
            party = SelectField('Party', choices = lst)
            submit = SubmitField('Submit')
        return F()

class CongressmanSearchChamberForm():
    def form(lst):
        class F(FlaskForm):
            chamber = SelectField('Chamber', choices = lst)
            submit = SubmitField('Submit')
        return F()


class BillSearchForm():
    def form(lst):
        class F(FlaskForm):
            category = SelectField('Search Category', choices = lst)
            submit = SubmitField('Submit')
        return F()

class BillSearchCategoryForm():
    def form(lst):
        class F(FlaskForm):
            billCat = SelectField('Category', choices = lst)
            submit = SubmitField('Submit')
        return F()


class BillSearchIntroDateForm():
    def form(lst):
        class F(FlaskForm):
            introDateRange = SelectField('Introduction Date', choices = lst)
            submit = SubmitField('Submit')
        return F()

class BillSearchChamberForm():
    def form(lst):
        class F(FlaskForm):
            chamb = SelectField('Chamber', choices = lst)
            submit = SubmitField('Submit')
        return F()



class UserRepChoiceForm():
    def form(rep_lst):
        class F(FlaskForm):
            cman = SelectField('Congressman', choices = rep_lst)
            submit = SubmitField('Submit')
            
        return F()

class UserRepVoteDecisionForm():
    def form(dec_lst):
        class F(FlaskForm):
            decision = SelectField('Decision', choices = dec_lst)
            submit = SubmitField('Submit')
            
        return F()

