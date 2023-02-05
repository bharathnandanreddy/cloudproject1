from flask import Flask
from flask_login import LoginManager
from models import db





app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite'

db.init_app(app)

# See important note below
from models import User

with app.app_context():
    db.create_all() 
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# blueprint for auth routes in our app
from authfile import auth
app.register_blueprint(auth)

# blueprint for non-auth parts of app
from mainfile import main
app.register_blueprint(main)
if __name__ == "__main__":
    app.run()
