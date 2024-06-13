from flask import Flask, json, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, current_user
from config import Development
from flask_migrate import Migrate
# from flask_mail import Mail
# from flask_moment import Moment








app = Flask(__name__)

app.config.from_object(Development)

# ================= CONFIGS_OF_LOGIN_MANAGER ==========================
# login = LoginManager()
# login.login_view = 'login'
# login.login_message_category = 'info'
# login.init_app(app)
# ====================================================================



db = SQLAlchemy(app)

migrate = Migrate(app, db, compare_type=True)

# mail = Mail(app)

# moment = Moment(app)

# ckeditor = CKEditor(app) 







@app.route('/')
def home():
    return render_template('home.html')






# -------------------------- blueprint settings --------------------
from admin import admin
from auth import auth


app.register_blueprint(admin)
app.register_blueprint(auth)

# ------------------------------------------------------------------






@app.errorhandler(404)
def NotFound(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def NotRespond(error):
    return render_template('500.html', error=error)



if __name__ == '__main__':
    app.run()