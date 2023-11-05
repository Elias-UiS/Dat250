"""Provides the app package for the Social Insecurity application. The package contains the Flask app and all of the extensions and routes."""

from pathlib import Path
from typing import cast

from flask import Flask
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app.config import Config
from app.database import SQLite3
from flask_bcrypt import Bcrypt, generate_password_hash
from flask_talisman import Talisman

# from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

# Instantiate and configure the app
app = Flask(__name__)
app.config.from_object(Config)
secret_key = app.config["SECRET_KEY"]

# Instantiate the sqlite database extension
sqlite = SQLite3(app, schema="schema.sql")

# : Handle login management better, maybe with flask_login?
login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
     user = sqlite.query(f"SELECT * FROM Users WHERE id = {id};", one=True)
     if user is None:
          return None
     else:
          user_class = User(user["id"], user["username"], user["password"])
          return user_class
    

class User(UserMixin):
    def __init__(self, id, username, password):
         self.id = id
         self.username = username
         self.password = password

    def is_anonymous(self):
         return False
    def is_authenticated(self):
         return True
    def is_active(self):
         return True
    def get_id(self):
          try:
               return str(self.id)
          except AttributeError:
               raise NotImplementedError("No `id` attribute - override `get_id`") from None
    
# : The passwords are stored in plaintext, this is not secure at all. I should probably use bcrypt or something
bcrypt = Bcrypt(app)

# : The CSRF protection is not working, I should probably fix that
csrf = CSRFProtect(app)
app.config['CSRF_ENABLED'] = True



# Create the instance and upload folder if they do not exist
with app.app_context():
    instance_path = Path(app.instance_path)
    if not instance_path.exists():
        instance_path.mkdir(parents=True, exist_ok=True)
    upload_path = instance_path / cast(str, app.config["UPLOADS_FOLDER_PATH"])
    if not upload_path.exists():
        upload_path.mkdir(parents=True, exist_ok=True)

# Import the routes after the app is configured
from app import routes  # noqa: E402,F401
