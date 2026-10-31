from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    Optional,
    Regexp,
    ValidationError,
)

from rdmanager.models import Customer, Terminal


def blank_to_none(value):
    # Blank fields are stored as NULL, so the unique e-mail allows many empty ones
    return (value.strip() or None) if isinstance(value, str) else value


def remove_spaces(value):
    # IDs are usually pasted as shown by RustDesk ("123 456 789")
    return "".join(value.split()) if isinstance(value, str) else value


class CustomerForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired(message="Name field is mandatory"), Length(max=100)],
    )
    email = StringField(
        "E-Mail",
        filters=[blank_to_none],
        validators=[Optional(), Email(message="Invalid e-mail"), Length(max=120)],
    )
    phone = StringField(
        "Phone",
        filters=[remove_spaces, blank_to_none],
        validators=[
            Optional(),
            Regexp(r"^\d+$", message="Phone must contain only digits"),
            Length(max=11),
        ],
    )
    address = StringField(
        "Address", filters=[blank_to_none], validators=[Optional(), Length(max=100)]
    )
    number = IntegerField("Number", validators=[Optional()])
    complement = StringField(
        "Complement", filters=[blank_to_none], validators=[Optional(), Length(max=25)]
    )
    city = StringField(
        "City", filters=[blank_to_none], validators=[Optional(), Length(max=100)]
    )
    state = StringField(
        "State", filters=[blank_to_none], validators=[Optional(), Length(max=2)]
    )
    postal_code = StringField(
        "Postal code",
        filters=[blank_to_none],
        validators=[Optional(), Length(max=10)],
    )
    submit = SubmitField("Save")

    def __init__(self, customer=None, *args, **kwargs):
        super().__init__(*args, obj=customer, **kwargs)
        self.customer = customer

    def validate_email(self, email):
        existing = Customer.query.filter_by(email=email.data).first()
        if existing and existing is not self.customer:
            raise ValidationError("This e-mail is already registered")


class TerminalForm(FlaskForm):
    description = StringField(
        "Description", filters=[blank_to_none], validators=[Optional(), Length(max=50)]
    )
    rustdesk_id = StringField(
        "RustDesk ID",
        filters=[remove_spaces],
        validators=[
            DataRequired(message="RustDesk ID field is mandatory"),
            Length(max=12),
        ],
    )
    rustdesk_password = StringField(
        "RustDesk password",
        validators=[
            DataRequired(message="RustDesk password field is mandatory"),
            Length(max=12),
        ],
    )
    submit = SubmitField("Save")

    def __init__(self, terminal=None, *args, **kwargs):
        super().__init__(*args, obj=terminal, **kwargs)
        self.terminal = terminal

    def validate_rustdesk_id(self, rustdesk_id):
        existing = Terminal.query.filter_by(rustdesk_id=rustdesk_id.data).first()
        if existing and existing is not self.terminal:
            raise ValidationError("This RustDesk ID is already registered")


class DeleteForm(FlaskForm):
    submit = SubmitField("Remove")
