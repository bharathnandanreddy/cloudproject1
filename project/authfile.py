from flask import Blueprint,flash,render_template,redirect,url_for,request
from models import db
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user,login_required, logout_user
from fileinput import filename
import calendar
import time


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, False)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')
@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    username = request.form.get('username')
    password = request.form.get('password')
    count=0
    filename=""
    f = request.files['file']
    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)
    if f.filename!="" and f.filename!=None:
        filename=str(time_stamp)+'_'+f.filename
        f.save('project/static/'+filename)
        with open('project/static/'+filename) as f:
            text = f.read()
            count=len(text.split())
        
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    
    user = User.query.filter_by(username=username).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Username address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, count=count, filename=filename, fname=fname, lname=lname, username=username, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
