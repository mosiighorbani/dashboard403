from . import auth
from flask import render_template




@auth.route('register', methods=['POST', 'GET'])
def register():
    return render_template('auth/register.html')


@auth.route('login', methods=['POST', 'GET'])
def login():
    return render_template('auth/login.html')