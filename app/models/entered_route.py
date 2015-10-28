from mongoengine import *

__all__ = ['EnteredRoute']


class EnteredRoute(Document):
    user = ObjectIdField(required=True)
    route = ObjectIdField(required=True)
    percentage = IntField(default=0)
    attach_complete = ListField(ObjectIdField())


