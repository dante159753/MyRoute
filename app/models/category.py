from mongoengine import *

__all__ = ['Category']


class Category(Document):
    title = StringField(required=True)
    desc = StringField(required=True, max_length=200)
    icon = FileField()
    father = ObjectIdField()
    sons = ListField(ObjectIdField())
    routes = ListField(ObjectIdField())

