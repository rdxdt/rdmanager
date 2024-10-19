from flask import Blueprint, render_template, url_for, flash, redirect, request
from rdmanager import app, db, bcrypt, ip_ban
from rdmanager.main.forms import LoginForm
from rdmanager.models import User, UserLogins
from flask_login import login_user, current_user, logout_user


main = Blueprint('main',__name__)

@main.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))
    else:
        return redirect('/admin')

@main.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/admin') 
    ip_ban.add(ip=request.remote_addr,url=url_for('main.login'))
    logform = LoginForm()
    if logform.validate_on_submit():
        user = User.query.filter_by(email=logform.Email.data).first()
        print(user)
        if user and bcrypt.check_password_hash(user.password_hash, logform.Password.data):
            login_user(user, remember=logform.remember.data)
            loginrec = UserLogins(user_id= user.id, login_ip= request.remote_addr)
            db.session.add(loginrec)
            db.session.commit()
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Não foi possível efetuar login com esse e-mail e senha.')    
    return render_template('login.html',title='Login',form=logform) 

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))