__author__ = 'Dante <wyz159753@gmail.com>'

__all__ = ['app', 'login_manager']


from flask import Flask
from flask_restful import Resource, Api
from flask.ext.login import LoginManager
from mongoengine import connect


# init app and restful api
app = Flask(__name__)
api = Api(app)

# read config
app.config.from_object('config_default')

# init login manager
login_manager = LoginManager()
login_manager.init_app(app)

# init db
connect(
    app.config['MONGODB_DB'],
    host=app.config['MONGODB_HOST'],
    alias='default'
)


from .resources.home import blueprint
app.register_blueprint(blueprint, url_prefix='')
del blueprint

from .resources.user import blueprint
app.register_blueprint(blueprint, url_prefix='/user')
del blueprint

print app.url_map

