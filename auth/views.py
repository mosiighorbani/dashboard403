import uuid
import random
from . import auth
from flask import render_template, request, redirect, url_for, flash
from .models import UserModel
from .forms import RegisterForm, LoginForm, PhoneForm, AuthPhoneForm, PasswordForm
from app import db
from flask_login import login_user, current_user, logout_user
from datetime import datetime






@auth.route('register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        flash('you are logged previously', 'success')
        return redirect(url_for('admin.index'))
    form = RegisterForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('your form is invalid', 'danger')
            return redirect(url_for('auth.register'))
        # ........................................................
        name = request.form.get('name')
        phone = request.form.get('phone')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        # ........................................................
        if  password != password_confirm:
            flash('your password and confirm password is not equal', 'danger')
            return redirect(url_for('auth.register'))
        user = UserModel()
        user.name = name
        user.phone = phone
        user.set_password(password)
        try:
            db.session.add(user)
            db.session.commit()
            flash('user is registered successfully', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Error {e} is happened, please try again', 'danger')
            db.session.rollback()
            return redirect(url_for('auth.register')) 
    #  GET Request
    return render_template('auth/register.html', form=form)


@auth.route('login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        flash('you are logged previously', 'success')
        return redirect(url_for('admin.index'))
    # 
    form = LoginForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('form is not valid, please try again', 'danger')
            return redirect(url_for('auth.login'))
        phone = request.form.get('phone')
        password = request.form.get('password')
        user = UserModel.query.filter_by(phone=phone).first()
        if not user:
            flash('this phone is not registered yet, please register now', 'danger')
            return redirect(url_for('auth.login'))
        if not user.check_password(password):
            flash('your password is incorrect', 'danger')
            return redirect(url_for('auth.login'))
        user.login_at = datetime.now()
        db.session.commit()
        db.session.flush()
        login_user(user)
        flash(f'Welcome {user.name} to admin panel', 'success')
        return redirect(url_for('admin.index'))
    # GET Request
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    current_user.logout_at = datetime.now()
    db.session.commit()
    db.session.flush()
    flash(f'{current_user.name} is logged out successfully', 'warning')
    logout_user()
    return redirect(url_for('auth.login'))



@auth.route('forgot-pass', methods=['POST', 'GET'])
def forgot_pass():
    if current_user.is_authenticated:
        flash('you are logged previously', 'success')
        return redirect(url_for('admin.index'))
    form = PhoneForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('your phone number is incorrect', 'warning')
            return redirect(url_for('auth.forgot_pass'))
        phone = request.form.get('phone')
        user = UserModel.query.filter_by(phone=phone).first()
        if not user:
            flash('this phone number is not registered yet', 'danger')
            return redirect(url_for('auth.forgot_pass'))
        token = str(uuid.uuid4().hex)
        code = random.randint(100000, 999999)
        try:
            user.token = token
            user.code = code
            db.session.commit()
            db.session.flush()
        except:
            flash('An Error is happened, please try again', 'warning')
            return redirect(url_for('auth.forgot_pass'))
        print('code is : ', code)
        return redirect(url_for('auth.auth_phone', token=token))
    
    return render_template('auth/forgot-pass.html', form=form)


@auth.route('auth-phone', methods=['POST', 'GET'])
def auth_phone():
    token = request.args.get('token')
    form = AuthPhoneForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('your code is not valid', 'warning')
            return redirect(url_for('auth.auth_phone'))
        user = UserModel.query.filter_by(token=token).first()
        if not user:
            flash('eneter values is incorrect, please try again', 'danger')
            return redirect(url_for('auth.forgot_pass'))
        auth_code = request.form.get('code')
        if str(auth_code) != str(user.code):
            flash('your code is incorrect', 'danger')
            return redirect(url_for('auth.auth_phone', token=token))
        flash('your code is correct', 'success')
        return redirect(url_for('auth.change_pass', token=token))
        
    return render_template('auth/auth-phone.html', form=form, token=token)


@auth.route('chnage-pass', methods=['POST', 'GET'])
def change_pass():
    token = request.args.get('token')
    user = UserModel.query.filter_by(token=token).first()
    form = PasswordForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash(f'your form is incorrect, {form.errors}', 'danger')
            return redirect(url_for('auth.change_pass', token=token))
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        if password != password_confirm:
            flash('your password and confirm password is not equal', 'warning')
            return redirect(url_for('auth.change_pass', token=token))
        try:
            user.set_password(password)
            user.token = None
            user.code = None
            user.updated_at = datetime.now()
            db.session.commit()
            db.session.flush()
            flash('your password is changed successfully', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Error {e} is happened, please try again', 'warning')
            return redirect(url_for('auth.change_pass', token=token))

    return render_template('auth/change-pass.html', form=form, token=token)