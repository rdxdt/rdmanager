import os

from flask import Blueprint, render_template, url_for, flash, redirect, request, session
from sqlalchemy import inspect
from rdmanager import app, db, bcrypt, ip_ban, hcaptcha
from rdmanager.main.forms import (
    LoginForm,
    InstallForm,
    ResetRequestForm,
    ResetCodeForm,
    ResetPasswordForm,
)
from rdmanager.main.utils import send_reset_email, verify_reset_code
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


@main.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = ResetRequestForm()
    if form.validate_on_submit():
        if not hcaptcha.verify():
            flash("Captcha verification failed, please try again.")
        else:
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                send_reset_email(user)
            # Same response for unknown e-mails so registered ones can't be discovered
            session["reset_email"] = form.email.data
            flash("If the e-mail is registered, a recovery code has been sent to it.")
            return redirect(url_for("main.reset_verify"))
    return render_template("main/reset_request.html", title="Password recovery", form=form)


@main.route("/reset_password/verify", methods=["GET", "POST"])
def reset_verify():
    # The e-mail link carries the e-mail and code in the query string
    if "email" in request.args:
        session["reset_email"] = request.args["email"]
    email = session.get("reset_email")
    if not email:
        return redirect(url_for("main.reset_request"))
    form = ResetCodeForm()
    code = form.code.data if form.validate_on_submit() else request.args.get("code")
    if code:
        user = User.query.filter_by(email=email).first()
        if user and verify_reset_code(user, code):
            session["reset_code"] = code
            return redirect(url_for("main.reset_password"))
        # Count failed attempts so the code can't be brute forced from one IP
        ip_ban.add(ip=request.remote_addr, url=url_for("main.reset_verify"))
        flash("Invalid or expired code.", "danger")
    return render_template("main/reset_verify.html", title="Password recovery", form=form, email=email)


@main.route("/reset_password/new", methods=["GET", "POST"])
def reset_password():
    # The code is checked again so it can't be used after it expires
    user = User.query.filter_by(email=session.get("reset_email")).first()
    if not user or not verify_reset_code(user, session.get("reset_code", "")):
        flash("The recovery code has expired, please request a new one.", "danger")
        return redirect(url_for("main.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        session.pop("reset_email")
        session.pop("reset_code")
        flash("Your password has been changed, login to continue.", "success")
        return redirect(url_for("main.login"))
    return render_template("main/reset_password.html", title="New password", form=form)