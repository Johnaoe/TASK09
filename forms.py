from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
import mod

MESSAGE_BAD_EMAIL = 'Wrong email address'

class RegForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    email = StringField('E.Mail', [DataRequired(), Email()])
    passw = PasswordField('Pasword', [DataRequired()])
    confirm = PasswordField('Repeat Password', [EqualTo('passw'), 'Passwords must be matching'])
    submit = SubmitField('Register')

    def match_name(self, name):
        user = mod.User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('User name is taken, choose other user name')
        
    def match_email(self, email):
        user = mod.User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is in user, choose other email')

class LoginForm(FlaskForm):
    email = StringField('Email', [DataRequired(), Email('BAD_EMAIL')])
    passw = PasswordField('Password', [DataRequired()])
    stay = BooleanField('Remember me')
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    email = StringField('Email', [DataRequired(), Email(MESSAGE_BAD_EMAIL)])
    submit = SubmitField('Renew')

    def match_name(form, name):
        user = mod.User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('User name is taken, choose other user name')

    def match_email(form, email):
        user = mod.User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is in user, choose other email')


class CarRegister(FlaskForm):
    brand = StringField('Brand', [DataRequired()])
    model = StringField('Model', [DataRequired()])
    years = IntegerField('Production years', [DataRequired()])
    engin = StringField('car Engine', [DataRequired()])
    number = StringField('Number Plate', [DataRequired()])
    vin_nr = StringField('VIN code', [DataRequired()])
    submit = SubmitField('Sumbmit your car')

    def vin_check(form, vin_nr):
        car = mod.Cars.query.filter_by(vin_nr=vin_nr.data).first()
        print("____________", car)
        if car:
            raise ValidationError('Car is already exists')

class RepairOrderForm(FlaskForm):
    issues = TextAreaField('Issue', [DataRequired()])
    submit = SubmitField('Register service')

class ServiceSatus(FlaskForm):
    status = SelectField('Status', choices=["New", "Accepted", "Taken", "On Hold", "Done", "Finished"])
    prices = IntegerField('Price', [DataRequired()])
    issues = TextAreaField('Issue', [DataRequired()])
    submit = SubmitField('Submit')