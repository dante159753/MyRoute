from mongoengine import *

__all__ = ['Route']


class Route(Document):
    title = StringField(required=True)
    father = ObjectIdField(required=False)
    author = ObjectIdField(required=True)
    n_upvote = IntField(required=True, default=0)
    n_entered = IntField(required=True, default=0)
    last_change_ts = IntField(required=False)
    create_ts = IntField(required=True)
    md_file = FileField(required=True)
    attached = ListField(ObjectIdField())


