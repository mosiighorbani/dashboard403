from . import admin
from flask import render_template




@admin.route('', methods=['POST', 'GET'])
def index():
    return render_template('admin/dashboard.html')