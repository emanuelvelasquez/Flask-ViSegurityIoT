from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask import render_template, Flask
import os
import time


#local import
from config import app_config

#inicializa db y login
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate(compare_type=True)
mail=Mail()
#sched = BackgroundScheduler(daemon=True)

def create_app(config_name):
    if os.getenv('FLASK_CONFIG') == "production":
        app = Flask(__name__)
        app.config.update(
            SECRET_KEY=os.getenv('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI'),
            MAIL_SERVER = 'smtp.gmail.com',
            MAIL_PORT = 465,
            MAIL_USERNAME = 'visegurityiot@gmail.com',
            MAIL_PASSWORD = 'jfvdxflqqrxwpwbi',
            DONT_REPLY_FROM_EMAIL = '(Vi-Segurity-IoT, visegurityiot@gmail.com)',
            MAIL_USE_SSL= True,
            MAIL_USE_TLS = False

        )
    else:
        app = Flask(__name__, instance_relative_config=True)
        app.config.from_object(app_config[config_name])
        app.config.from_pyfile('config.py')

    db.init_app(app)
   
    login_manager.init_app(app)
    login_manager.login_message = "Debes Iniciar Sesion!!!"
    login_manager.login_view = "auth.login"    

    migrate = Migrate(app, db)
    mail.init_app(app) 
    Bootstrap(app)
    
    #sched.start()
    

    from app import models

    from .administrador import administrador as administrador_blueprint
    app.register_blueprint(administrador_blueprint, url_prefix='/administrador')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .videostream import videostream as videostream_blueprint
    app.register_blueprint(videostream_blueprint)


    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html',title="Error-403"),403
    
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html", title=" Error-404"),404

    @app.errorhandler(500)
    def  error_server(error):
        return render_template('errors/500.html',title='Error-500'),500
    
    return app
