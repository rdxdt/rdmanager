from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    Optional,
    ValidationError,
)

from rdmanager.models import User


class UserForm(FlaskForm):
    # The user being edited, so its own e-mail isn't reported as already taken
    user = None

    name = StringField(
        "Name",
        validators=[DataRequired(message="Name field is mandatory"), Length(max=20)],
    )
    lastname = StringField(
        "Last name",
        validators=[
            DataRequired(message="Last name field is mandatory"),
            Length(max=50),
        ],
    )
    email = StringField(
        "E-Mail",
        validators=[
            DataRequired(message="E-mail field is mandatory"),
            Email(message="Invalid e-mail"),
            Length(max=120),
        ],
    )

    def validate_email(self, email):
        existing = User.query.filter_by(email=email.data).first()
        if existing and existing is not self.user:
            raise ValidationError("This e-mail is already registered")


class NewUserForm(UserForm):
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password field is mandatory"),
            Length(
                min=8,
                max=30,
                message="Password must be between 8 to 30 characters long",
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirm password",
        validators=[EqualTo("password", message="Passwords must match")],
    )
    submit = SubmitField("Create user")


class EditUserForm(UserForm):
    password = PasswordField(
        "New password",
        validators=[
            Optional(),
            Length(
                min=8,
                max=30,
                message="Password must be between 8 to 30 characters long",
            ),
        ],
        description="Leave blank to keep the current password.",
    )
    confirm_password = PasswordField(
        "Confirm new password",
        validators=[EqualTo("password", message="Passwords must match")],
    )
    submit = SubmitField("Save changes")

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, obj=user, **kwargs)
        self.user = user


class DeleteUserForm(FlaskForm):
    submit = SubmitField("Remove")
