from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ipban import IpBan
from flask_mail import Mail
from flask_admin import Admin
from rdmanager.config import Config
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.config.from_object(Config)
ip_ban = IpBan(ban_seconds=200)
ip_ban.init_app(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
mail = Mail(app)
app.wsgi_app = ProxyFix(app.wsgi_app,x_for=1,x_host=1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
admin = Admin(app,name='RDManager',template_mode='bootstrap4')

loginMgr = LoginManager(app)
loginMgr.login_view = 'main.login'
loginMgr.login_message = 'Login to continue'

from rdmanager.errors.handlers import errors
from rdmanager.main.routes import main
from rdmanager.admin_models import register_modelviews


app.register_blueprint(main)
app.register_blueprint(errors)

register_modelviews()
