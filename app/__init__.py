import os
from datetime import timedelta

from flask import Flask

from dotenv import load_dotenv
from flask_mail import Mail
from flask_login import LoginManager
from app.database.db_engine import init_db
from app.auditions.models.models import Base

load_dotenv()

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

init_db(Base)

app.permanent_session_lifetime = timedelta(hours=5)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['DOMAIN'] = os.environ.get('DOMAIN')

mail = Mail(app=app)

from .auditions.routes.test import test_blueprint
from .auditions.routes.auth import auth_blueprint
from .auditions.routes.admin import admin_blueprint
from .auditions.routes.auditions import audition_blueprint


app.register_blueprint(test_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(audition_blueprint)