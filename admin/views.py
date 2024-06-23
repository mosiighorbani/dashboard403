from . import admin
from flask import render_template, request
from auth.models import UserModel
from flask_login import login_required




@admin.route('', methods=['POST', 'GET'])
@login_required
def index():
    return render_template('admin/dashboard.html')


@admin.route('/users', methods=['POST', 'GET'])
@login_required
def users():
    # users = UserModel.query.all()
    page = request.args.get('page', default=1, type=int)
    users = UserModel.query.paginate(page=page, per_page=4)
    return render_template('admin/users.html', users=users)





# @admin.route('/users_query', methods=['GET'])
# @login_required
# def users_query():
#     page = request.args.get('page', default=1, type=int)
#     users = UserModel.query.paginate(page=page, per_page=4)
#     return users