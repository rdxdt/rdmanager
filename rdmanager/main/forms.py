from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,Regexp

class LoginForm(FlaskForm):
    Email=StringField('E-Mail',validators=[DataRequired(message='E-mail field is mandatory'),Email(message='Invalid e-mail')], render_kw={"placeholder": "Email"})
    Password=PasswordField('Password',validators=[DataRequired(message='Password field is mandatory'),Length(min=8,max=30,message='Password must be between 8 to 30 characters long')])
    Remember = BooleanField('Keep me logged in.')
    Submit=SubmitField('Login')

class InstallForm(FlaskForm):
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
    submit = SubmitField("Install")


class ResetRequestForm(FlaskForm):
    email = StringField(
        "E-Mail",
        validators=[
            DataRequired(message="E-mail field is mandatory"),
            Email(message="Invalid e-mail"),
        ],
    )
    submit = SubmitField("Send recovery code")


class ResetCodeForm(FlaskForm):
    code = StringField(
        "Recovery code",
        validators=[
            DataRequired(message="Code field is mandatory"),
            Regexp(r"^\d{6}$", message="The code must have 6 digits"),
        ],
        render_kw={"inputmode": "numeric", "autocomplete": "one-time-code"},
    )
    submit = SubmitField("Verify code")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "New password",
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
        "Confirm new password",
        validators=[EqualTo("password", message="Passwords must match")],
    )
    submit = SubmitField("Change password")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(
        "Current password",
        validators=[DataRequired(message="Current password field is mandatory")],
    )
    password = PasswordField(
        "New password",
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
        "Confirm new password",
        validators=[EqualTo("password", message="Passwords must match")],
    )
    submit = SubmitField("Change password")
