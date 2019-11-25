from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, logout_user
from flask_security import login_required

from sqlalchemy import *
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
    return db.session.query(models.RegisteredUser).filter(models.RegisteredUser.email == user_id).first()

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    registereduser = db.session.query(models.RegisteredUser).all()
    states = sorted(set([x[0] for x in db.session.query(models.Congressman.state).all()]))
    states = [(x,x) for x in states]
    form = forms.RegisterForm.form(states)
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            models.RegisteredUser.create(form.name.data, form.email.data, form.password.data, form.state.data, form.district.data)
            flash('Thanks for registering! Please log in now.', 'success')
            return redirect(url_for('login'))
        except:
            flash('ERROR! Email ({}) already exists.'.format(form.email.data), 'error')
    else: 
        flash('All fields are required. Make sure you input a valid email.')
    return render_template('register.html', form=form)


#NEED TO THINK ABOUT WHERE TO GO FROM LOGIN PAGE
@app.route('/login', methods = ['GET','POST'])
def login():
    form = forms.LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = db.session.query(models.RegisteredUser).filter_by(email=form.email.data).first()
            if user is not None and user.is_correct_password(form.password.data):
                user.authenticated = True
                db.session.add(user)
                login_user(user)
                flash('Thanks for logging in, {}'.format(current_user.name))
                return redirect(url_for('user', email = current_user.email))
            else:
                flash('ERROR! Incorrect login credentials.', 'error')
    return render_template('login.html', form=form)

#MIGHT WANT TO CHANGE RENDER LATER
@app.route("/logout")
def logout():
    user = current_user
    user.authenticated = False
    # db.session.add(user)
    logout_user()
    flash('Successfully logged out!', 'info')
    return redirect(url_for('login'))

@app.route("/update", methods = ['GET', 'POST'])
def update_user():
    user = current_user
    paststate = current_user.state
    states = sorted(set([x[0] for x in db.session.query(models.Congressman.state).all()]))
    states = [(x,x) for x in states]
    form = forms.UpdateForm.form(states, paststate)
    if request.method == 'POST':
        current_user.update(form.name.data, form.password.data, form.state.data, form.district.data)
        flash("Information successfully updated, {}.".format(current_user.name), 'success')
        return redirect(url_for('homepage'))

    return render_template('update-userinfo.html', form=form)



@app.route('/homepage/congressman-search', methods = ['GET','POST'])
def congressman_search():
    lst = [('all', 'Display All'), ('name', 'Name'), ('state_territory_district', 'State/Territory/District'), ('party', 'Party'), ('chamber', 'Chamber')]
    form = forms.CongressmanSearchForm.form(lst)
    if request.method == 'POST':
        if form.category.data == 'all':
            return redirect(url_for('all_congressman'))
        return redirect(url_for('congressman_search_' + form.category.data))
    return render_template('congressman-search.html', form = form)

@app.route('/homepage/congressman-search-name', methods = ['GET', 'POST'])
def congressman_search_name():
    form = forms.CongressmanSearchNameForm.form()
    if request.method == 'POST':
        search = "%{}%".format(form.name.data)
        cmen = db.session.query(models.Congressman).filter(models.Congressman.name.ilike(search)).all()
        return render_template('congressman-search-name.html', form=form, allcongressman=cmen)
    return render_template('congressman-search-name.html', form = form, allcongressman = [])

@app.route('/homepage/congressman-search-state-territory-district', methods = ['GET', 'POST'])
def congressman_search_state_territory_district():
    states = sorted(set([x[0] for x in db.session.query(models.Congressman.state).all()]))
    states = [(x,x) for x in states]
    form = forms.CongressmanSearchStateTerritoryDistrictForm.form(states)
    if request.method == 'POST':
        if form.district.data is None:
            cmen = db.session.query(models.Congressman).filter(models.Congressman.state == form.state.data).all()
            return render_template('congressman-search-state-territory-district.html', form=form, allcongressman = cmen)
        else:
            cmen = db.session.query(models.Congressman).filter(models.Congressman.state == form.state.data, or_(models.Congressman.district == form.district.data, models.Congressman.house_or_senate == 'sen'))
            return render_template('congressman-search-state-territory-district.html', form=form, allcongressman = cmen)
    return render_template('congressman-search-state-territory-district.html', form = form, allcongressman = [])

@app.route('/homepage/congressman-search-party', methods = ['GET','POST'])
def congressman_search_party():
    parties = sorted(set([x[0] for x in db.session.query(models.Congressman.party).all()]))
    parties = [(x,x) for x in parties]
    form = forms.CongressmanSearchPartyForm.form(parties)
    if request.method == 'POST':
        cmen = db.session.query(models.Congressman).filter(models.Congressman.party == form.party.data).all()
        return render_template('congressman-search-party.html', form=form, allcongressman = cmen)
    return render_template('congressman-search-party.html', form = form, allcongressman = [])

@app.route('/homepage/congressman-search-chamber', methods = ['GET', 'POST'])
def congressman_search_chamber():
    chambers = [('rep', 'House of Representatives'), ('sen', 'Senate')]
    form = forms.CongressmanSearchChamberForm.form(chambers)
    if request.method == 'POST':
        cmen = db.session.query(models.Congressman).filter(models.Congressman.house_or_senate == form.chamber.data).all()
        return render_template('congressman-search-chamber.html', form=form, allcongressman = cmen)
    return render_template('congressman-search-chamber.html', form = form, allcongressman = [])

@app.route('/homepage/all-congressman')
def all_congressman():
    cman = db.session.query(models.Congressman).all()
    return render_template('all-congressman.html', allcongressman=cman)

#TEMPORARY FOR DEBUGGING
@app.route('/homepage/all-users')
def all_users():
    cuser = db.session.query(models.RegisteredUser).all()
    return render_template('all-users.html', alluser=cuser)

@app.route('/homepage/congressperson/<id>')
def congressperson(id):
    cperson = db.session.query(models.Congressman)\
        .filter(models.Congressman.id == id).one()
    bills = db.session.query(models.SponsoredBy).filter(models.SponsoredBy.rep_id == id).all()
    return render_template('congressperson.html', congressperson=cperson, bills = bills)

@app.route('/homepage/user/<email>')
def user(email):
    cuser = db.session.query(models.RegisteredUser)\
        .filter(models.RegisteredUser.email == email).one()

    sen = db.session.query(models.Congressman)\
        .filter(models.Congressman.state == cuser.state, models.Congressman.house_or_senate == "sen").all()
    
    rep = db.session.query(models.Congressman)\
        .filter(models.Congressman.state == cuser.state, models.Congressman.district == cuser.district, models.Congressman.house_or_senate == "rep").all()

    rep_votes = db.session.query(models.Vote)\
        .filter(models.Vote.rep_id.in_(rep)).all()

    return render_template('user.html', user = cuser, senator = sen, representative = rep, votes_by_rep = rep_votes)

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
