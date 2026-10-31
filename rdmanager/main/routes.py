import os

from flask import Blueprint, render_template, url_for, flash, redirect, request
from sqlalchemy import inspect
from rdmanager import app, db, bcrypt, ip_ban, hcaptcha
from rdmanager.main.forms import LoginForm, InstallForm
from rdmanager.models import User, UserLogins, Customer, Terminal
from flask_login import login_user, current_user, logout_user, login_required


main = Blueprint('main',__name__)


def is_installed():
    url = db.engine.url
    if url.get_backend_name() == "sqlite":
        # Checked on disk because connecting to SQLite would create the file
        return os.path.exists(url.database)
    existing_tables = set(inspect(db.engine).get_table_names())
    return set(db.metadata.tables).issubset(existing_tables)


@main.route("/install", methods=["GET", "POST"])
def install():
    if is_installed():
        return redirect(url_for("main.home"))
    form = InstallForm()
    if form.validate_on_submit():
        # Tables are only created on submit, otherwise the SQLite file created
        # on GET would make the POST be redirected as already installed
        db.create_all()
        user = User(
            name=form.name.data,
            lastname=form.lastname.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        flash("Installation complete, login to continue.")
        return redirect(url_for("main.login"))
    return render_template("main/install.html", title="Install", form=form)

@main.route('/')
@login_required
def home():
    # The newest record is the current session, so skip it to show the previous login
    last_login = (
        UserLogins.query.filter_by(user_id=current_user.id)
        .order_by(UserLogins.login_date.desc())
        .offset(1)
        .first()
    )
    return render_template(
        "main/home.html",
        title="Home",
        last_login=last_login,
        customer_count=Customer.query.count(),
        terminal_count=Terminal.query.count(),
    )

@main.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    ip_ban.add(ip=request.remote_addr,url=url_for('main.login'))
    logform = LoginForm()
    if logform.validate_on_submit():
        user = User.query.filter_by(email=logform.Email.data).first()
        if not hcaptcha.verify():
            flash("Captcha verification failed, please try again.")
        elif user and bcrypt.check_password_hash(user.password_hash, logform.Password.data):
            login_user(user, remember=logform.Remember.data)
            loginrec = UserLogins(user_id= user.id, login_ip= request.remote_addr)
            db.session.add(loginrec)
            db.session.commit()
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Login failed, check the username and password and try again.')    
    return render_template('main/login.html',title='Login',form=logform)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))