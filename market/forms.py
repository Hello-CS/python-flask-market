#Creating forms with libraries flask-wtf and wtforms
#we use classes to make our forms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField #for special inputs like string, integer, etc
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):
    #FLaskForm can understand certain functions with specific names such as validate_
    #It then checks after _ aka username and checks if there is a field.
    #So, there is an auto validation and we don't need to implement it
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists!')
    
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email address already exists!')

    username = StringField(label='Username:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    #creating 2 fields for pw for confirmation via validation
    #Using the PasswordField from the library is more secure than StringField
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create account')

class LoginForm(FlaskForm):
    username = StringField(label="Username:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class PurchaseForm(FlaskForm):
    submit = SubmitField(label='Purchase')

class SellForm(FlaskForm):
    submit = SubmitField(label='Sell')