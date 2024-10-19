from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,Email

class LoginForm(FlaskForm):
    Email=StringField('E-Mail',validators=[DataRequired(message='E-mail field is mandatory'),Email(message='Invalid e-mail')], render_kw={"placeholder": "Email"})
    Password=PasswordField('Password',validators=[DataRequired(message='Password field is mandatory'),Length(min=8,max=30,message='Password must be between 8 to 30 characters long')])
    Remember = BooleanField('Keep me logged in.')
    Submit=SubmitField('Login')