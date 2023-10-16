"""
__init__.py

This module initializes the Flask application and configures key components such as the database, migrations, and user login management.

Contents:
- Initialization of the Flask application.
- Configuration of application settings using the `Config` object from the `config.py` module.
- Setup of the SQLAlchemy database connection using Flask-SQLAlchemy.
- Configuration of database migrations with Flask-Migrate.
- Configuration of user login management with Flask-Login.
- Import of routes and models from the app package.
"""

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager  

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)  
login.login_view = 'login' 

from app import routes, models

