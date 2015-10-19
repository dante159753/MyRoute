from flask import Blueprint
from flask-restful import Api

__all__ = [
    'blueprint'
]

blueprint = Blueprint('category', __name__)
api = Api(blueprint)


from .category import CategoryRes
api.add_resource(CategoryRes, '/category/')
del CategoryRes


