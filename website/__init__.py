#from website.models import User, Income, Expense, Budget

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'the secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)


    from .views import views
    from .auth import auth
    from .models import User
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    

    #create_database()

    login_manager = LoginManager()
    login_manager.login_view= 'auth.sign_in'  # type: ignore
    login_manager.init_app(app)

    #from .models import User # Income, Expense, Budget

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    with app.app_context(): #can remove this line if don't solve problem
        create_database()

    return app


def create_database():
    if not path.exists('website/' + DB_NAME):
            db.create_all()
            print('Created Database')
