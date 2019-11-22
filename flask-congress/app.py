from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_security import login_required

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
import forms

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': True})

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
 
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/homepage/register', methods = ['GET', 'POST'])
def register():
    
    registereduser = db.session.query(models.RegisteredUser).all()
    form = forms.RegisterForm.form(registereduser)

    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            models.RegisteredUser.create(form.name.data, form.email.data, form.state.data, form.district.data)
            flash('Thanks for registering!', 'success')
            return redirect(url_for('/'))
        except:
            # session.rollback
            flash('ERROR! Email ({}) already exists.'.format(form.email.data), 'error')
    return render_template('register.html', form=form)


#NEED TO THINK ABOUT WHERE TO GO FROM LOGIN PAGE
@app.route('/homepage/login')
def login():
    form = forms.LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None and user.is_correct_password(form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash('Thanks for logging in, {}'.format(current_user.email))
                return redirect(url_for('homepage'))
            else:
                session.rollback
                flash('ERROR! Incorrect login credentials.', 'error')
    return render_template('login.html', form=form)

#MIGHT WANT TO CHANGE RENDER LATER
@app.route("/logout")
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    flash('Goodbye!', 'info')
    return redirect(url_for('login'))

@app.route('/homepage/all-congressman')
def all_congressman():
    cman = db.session.query(models.Congressman).all()
    return render_template('all-congressman.html', allcongressman=cman)

@app.route('/homepage/all-users')
def all_users():
    cuser = db.session.query(models.RegisteredUser).all()
    return render_template('all-users.html', alluser=cuser)

@app.route('/homepage/congressperson/<name>')
def congressperson(name):
    cperson = db.session.query(models.Congressman)\
        .filter(models.Congressman.name == name).one()
    return render_template('congressperson.html', congressperson=cperson)

@app.route('/homepage/all-bill/')
def all_bill():
    bill = db.session.query(models.Bill).all()
    return render_template('all-bill.html', allbill=bill)
#
@app.route('/homepage/bills/<num>/<type>/<cong_year>')
def bills(num, type, cong_year):
    bnum = db.session.query(models.Bill)\
        .filter(models.Bill.num == num, models.Bill.type ==type, models.Bill.cong_year == cong_year).one()
    return render_template('bills.html', bills=bnum)


@app.route('/edit-drinker/<name>', methods=['GET', 'POST'])
def edit_drinker(name):
    drinker = db.session.query(models.Drinker)\
        .filter(models.Drinker.name == name).one()
    beers = db.session.query(models.Beer).all()
    bars = db.session.query(models.Bar).all()
    form = forms.DrinkerEditFormFactory.form(drinker, beers, bars)
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            models.Drinker.edit(name, form.name.data, form.address.data,
                                form.get_beers_liked(), form.get_bars_frequented())
            return redirect(url_for('drinker', name=form.name.data))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('edit-drinker.html', drinker=drinker, form=form)
    else:
        return render_template('edit-drinker.html', drinker=drinker, form=form)

@app.template_filter('pluralize')
def pluralize(number, singular='', plural='s'):
    return singular if number in (0, 1) else plural



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
