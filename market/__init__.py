from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '945eb18a5cb7be7a62457329'

# DB
db = SQLAlchemy(app)
# パスワードハッシュ
bcrypt = Bcrypt(app)
# ログイン認証
login_manager = LoginManager(app)

from market import routes
