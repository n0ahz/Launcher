__author__ = 'HZ'
#package

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask.ext.security import Security, SQLAlchemyUserDatastore
from celery import Celery
from flask.ext.babel import Babel


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# Initialize Flask-Mail
mail = Mail(app)

#Initialize Flask-Babel
babel = Babel(app)

# Setup Flask-Security
from models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Initialize Celery
celery_obj = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery_obj.conf.update(app.config)

from .import views, models

# change DEBUG in config
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    # Flask-Wergzeug requests logging
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
    logger = logging.getLogger('werkzeug')
    handler = RotatingFileHandler('launcher.log')
    handler.setFormatter(formatter)
    #handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    # Add the handler to Flask's logger for cases where Werkzeug isn't used as the underlying WSGI server.
    app.logger.addHandler(handler)