from flask import Flask, json, jsonify, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from config import Development
from flask_migrate import Migrate
# from flask_mail import Mail
# from flask_moment import Moment




app = Flask(__name__)

app.config.from_object(Development)

# ----------------------------- CONFIGS_OF_LOGIN_MANAGER -----------------------
login = LoginManager()
login.login_view = 'login'
login.login_message_category = 'info'
login.init_app(app)
# ------------------------------------------------------------------------------



db = SQLAlchemy(app)

# migrate = Migrate(app, db, compare_type=True)
migrate = Migrate(app, db)

# mail = Mail(app)

# moment = Moment(app)

# ckeditor = CKEditor(app) 








@app.route('/')
def home():
    flash("All OK", 'success')
    return jsonify({
        "dveloper" : "mosi",
        "language" : ['python', 'js'],
        "frameworks" : ['flask', 'bootstrap', 'html', 'alpinejs']
    })






# ........................ blueprint settings .......................
from admin import admin
from auth import auth


app.register_blueprint(admin)
app.register_blueprint(auth)

# ....................................................................



# ....................... login user handler ................................
from auth.models import User

@login.user_loader
def userLoader(user_id):
    return User.query.get(user_id)

@login.unauthorized_handler
def unauthorized():
    flash('You must login first', 'warning')
    return redirect(url_for('auth.login'))
# ...........................................................................



# .................... 404 $ 500 Error handler ...................
@app.errorhandler(404)
def NotFound(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def NotRespond(error):
    return render_template('500.html', error=error)
# ................................................................







if __name__ == '__main__':
    app.run()