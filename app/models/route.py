from mongoengine import *

__all__ = ['Route']


class Route(Document):
    father = ObjectIdField(required=True)
    n_upvote = IntField(required=True, default=0)
    n_entered = IntField(required=True, default=0)
    md_file = FileField(required=True)
    attached = ListField(ObjectIdField())


