from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site9.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'  # Cosmo

from flaskblog.models import User, Post, Sportsmen, Event, Comment

admin = Admin(app, name='Admin Page', template_mode='bootstrap3')
# admin = Admin(app)
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Sportsmen, db.session))
admin.add_view(ModelView(Event, db.session))
from flaskblog import routes
