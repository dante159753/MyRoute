from flask import Blueprint
from flask_restful import Api

__all__ = [
    'blueprint'
]

blueprint = Blueprint('home', __name__)
api = Api(blueprint)


from .home import HomeRes
api.add_resource(HomeRes, '/home/')
del HomeRes

