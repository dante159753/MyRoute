from mongoengine import *

__all__ = ['Category']


class Category(Document):
    desc = StringField(required=True, max_length=200)
    father = ObjectIdField()
    sons = ListField(ObjectIdField())
    routes = ListField(ObjectIdField())

