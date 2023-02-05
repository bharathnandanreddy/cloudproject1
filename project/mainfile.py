from flask import Blueprint
from flask import render_template
from flask_login import login_required, current_user
main = Blueprint('main', __name__)
import os
@main.route('/')
def index():
    
    return render_template('index.html',loggedin=current_user.is_authenticated)

@main.route('/profile')
@login_required
def profile():
    filename=current_user.filename
    if filename!="" and filename!=None:
        filename='http://ec2-52-86-81-249.compute-1.amazonaws.com/files/'+filename
    return render_template('profile.html',count=current_user.count, filename=filename, fname=current_user.fname,lname=current_user.lname, email=current_user.email, loggedin=current_user.is_authenticated)