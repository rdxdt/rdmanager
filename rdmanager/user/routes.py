from flask import Blueprint, render_template, url_for, flash, redirect, abort
from flask_login import current_user, login_required

from rdmanager import db
from rdmanager.models import User, UserLogins
from rdmanager.user.forms import NewUserForm, EditUserForm, DeleteUserForm

users = Blueprint("users", __name__, url_prefix="/users")

LOGINS_PER_PAGE = 10


@users.route("/")
@login_required
def list_users():
    user_list = User.query.order_by(User.name, User.lastname).all()
    return render_template(
        "user/list.html",
        title="Users",
        users=user_list,
        delete_form=DeleteUserForm(),
    )


@users.route("/new", methods=["GET", "POST"])
@login_required
def new_user():
    form = NewUserForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            lastname=form.lastname.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        flash("User created.", "success")
        return redirect(url_for("users.user_detail", user_id=user.id))
    return render_template("user/form.html", title="New user", form=form)


@users.route("/<int:user_id>")
@login_required
def user_detail(user_id):
    user = db.get_or_404(User, user_id)
    logins = (
        UserLogins.query.filter_by(user_id=user.id)
        .order_by(UserLogins.login_date.desc())
        .paginate(per_page=LOGINS_PER_PAGE, error_out=False)
    )
    return render_template(
        "user/detail.html",
        title=f"{user.name} {user.lastname}",
        user=user,
        logins=logins,
        delete_form=DeleteUserForm(),
    )


@users.route("/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    user = db.get_or_404(User, user_id)
    form = EditUserForm(user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.lastname = form.lastname.data
        user.email = form.email.data
        if form.password.data:
            user.password = form.password.data
        db.session.commit()
        flash("User updated.", "success")
        return redirect(url_for("users.user_detail", user_id=user.id))
    return render_template("user/form.html", title="Edit user", form=form, user=user)


@users.route("/<int:user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    if not DeleteUserForm().validate_on_submit():
        abort(400)
    # Removing yourself could leave the system without any user able to login
    if user.id == current_user.id:
        flash("You can't remove your own user.", "danger")
        return redirect(url_for("users.user_detail", user_id=user.id))
    UserLogins.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    flash("User removed.", "success")
    return redirect(url_for("users.list_users"))
