from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = 'b035407d9bb72797edceb8dcd9697492'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vece.db'

database: SQLAlchemy = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'home'
login_manager.login_message_category = 'alert-info'



from ProjetoVece import routes