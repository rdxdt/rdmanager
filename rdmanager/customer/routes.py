from flask import Blueprint, render_template, url_for, flash, redirect, abort
from flask_login import login_required

from rdmanager import db
from rdmanager.models import Customer, Terminal
from rdmanager.customer.forms import CustomerForm, TerminalForm, DeleteForm

customers = Blueprint("customers", __name__, url_prefix="/customers")


@customers.app_template_filter("rustdesk_id")
def format_rustdesk_id(rustdesk_id):
    # Grouped from the right like RustDesk does, so only the first group can be shorter
    first = len(rustdesk_id) % 3 or 3
    groups = [rustdesk_id[:first]]
    groups += [rustdesk_id[i : i + 3] for i in range(first, len(rustdesk_id), 3)]
    return " ".join(groups)


def get_terminal_or_404(customer_id, terminal_id):
    terminal = db.get_or_404(Terminal, terminal_id)
    # Keeps a terminal from being reached through another customer's URL
    if terminal.customer_id != customer_id:
        abort(404)
    return terminal


@customers.route("/")
@login_required
def list_customers():
    customer_list = Customer.query.order_by(Customer.name).all()
    return render_template(
        "customer/list.html",
        title="Customers",
        customers=customer_list,
        delete_form=DeleteForm(),
    )


@customers.route("/new", methods=["GET", "POST"])
@login_required
def new_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer()
        form.populate_obj(customer)
        db.session.add(customer)
        db.session.commit()
        flash("Customer created.", "success")
        return redirect(url_for("customers.customer_detail", customer_id=customer.id))
    return render_template("customer/form.html", title="New customer", form=form)


@customers.route("/<int:customer_id>")
@login_required
def customer_detail(customer_id):
    customer = db.get_or_404(Customer, customer_id)
    terminals = (
        Terminal.query.filter_by(customer_id=customer.id)
        .order_by(Terminal.description)
        .all()
    )
    return render_template(
        "customer/detail.html",
        title=customer.name,
        customer=customer,
        terminals=terminals,
        delete_form=DeleteForm(),
    )


@customers.route("/<int:customer_id>/edit", methods=["GET", "POST"])
@login_required
def edit_customer(customer_id):
    customer = db.get_or_404(Customer, customer_id)
    form = CustomerForm(customer)
    if form.validate_on_submit():
        form.populate_obj(customer)
        db.session.commit()
        flash("Customer updated.", "success")
        return redirect(url_for("customers.customer_detail", customer_id=customer.id))
    return render_template(
        "customer/form.html", title="Edit customer", form=form, customer=customer
    )


@customers.route("/<int:customer_id>/delete", methods=["POST"])
@login_required
def delete_customer(customer_id):
    customer = db.get_or_404(Customer, customer_id)
    if not DeleteForm().validate_on_submit():
        abort(400)
    Terminal.query.filter_by(customer_id=customer.id).delete()
    db.session.delete(customer)
    db.session.commit()
    flash("Customer removed.", "success")
    return redirect(url_for("customers.list_customers"))


@customers.route("/<int:customer_id>/terminals/new", methods=["GET", "POST"])
@login_required
def new_terminal(customer_id):
    customer = db.get_or_404(Customer, customer_id)
    form = TerminalForm()
    if form.validate_on_submit():
        terminal = Terminal(customer=customer)
        form.populate_obj(terminal)
        db.session.add(terminal)
        db.session.commit()
        flash("Terminal created.", "success")
        return redirect(url_for("customers.customer_detail", customer_id=customer.id))
    return render_template(
        "customer/terminal_form.html",
        title="New terminal",
        form=form,
        customer=customer,
    )


@customers.route(
    "/<int:customer_id>/terminals/<int:terminal_id>/edit", methods=["GET", "POST"]
)
@login_required
def edit_terminal(customer_id, terminal_id):
    terminal = get_terminal_or_404(customer_id, terminal_id)
    form = TerminalForm(terminal)
    if form.validate_on_submit():
        form.populate_obj(terminal)
        db.session.commit()
        flash("Terminal updated.", "success")
        return redirect(url_for("customers.customer_detail", customer_id=customer_id))
    return render_template(
        "customer/terminal_form.html",
        title="Edit terminal",
        form=form,
        customer=terminal.customer,
        terminal=terminal,
    )


@customers.route(
    "/<int:customer_id>/terminals/<int:terminal_id>/delete", methods=["POST"]
)
@login_required
def delete_terminal(customer_id, terminal_id):
    terminal = get_terminal_or_404(customer_id, terminal_id)
    if not DeleteForm().validate_on_submit():
        abort(400)
    db.session.delete(terminal)
    db.session.commit()
    flash("Terminal removed.", "success")
    return redirect(url_for("customers.customer_detail", customer_id=customer_id))
