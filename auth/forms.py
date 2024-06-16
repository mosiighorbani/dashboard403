from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from wtforms import PasswordField, StringField, EmailField, SelectField, SubmitField



class RegisterForm(FlaskForm):
    name = StringField('FullName', validators=[DataRequired(message='please enter your full name')])
    # email = EmailField('Email', validators=[DataRequired('email must be addedd'), Email('please enter valid email')])
    # email = EmailField('Email', validators=[Email('please enter valid email')])
    phone = StringField('PhoneNumber', validators=[DataRequired(message='please enter your phone number'), Length(min=11,max=11, message='please enter a valid phone number in Iran')])
    password = PasswordField('Password', validators=[DataRequired(message='please enter your password'), Length(min=8, message='please enter atleast 8 character')])
    password_confirm = PasswordField('PasswordConfirm', validators=[DataRequired(), EqualTo('password', message='please enter password confirm equal to password')])
    submit = SubmitField('RgisterBtn')


class LoginForm(FlaskForm):
    phone = StringField('PhoneNumber', validators=[DataRequired(message='please enter your phone number'), Length(min=11,max=11, message='please enter a valid phone number in Iran')])
    password = PasswordField('Password', validators=[DataRequired(message='please enter your password'), Length(min=8, message='please enter atleast 8 character')])
    submit = SubmitField('LoginBtn')


class PhoneForm(FlaskForm):
    phone = StringField('PhoneNumber', validators=[DataRequired(message='please enter your phone number'), Length(min=11,max=11, message='please enter a valid phone number in Iran')])
    submit = SubmitField('ForgotPassBtn')


class AuthPhoneForm(FlaskForm):
    code = StringField('CodeAuth', validators=[DataRequired(message='please enter your recieved code'), Length(min=6, max=6)])
    submit = SubmitField('PhoneAuthBtn')

class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(message='please enter your password'), Length(min=8, message='please enter atleast 8 character')])
    password_confirm = PasswordField('PasswordConfirm', validators=[DataRequired(), EqualTo('password', message='please enter password confirm equal to password')])
    submit = SubmitField('PasswordBtn')