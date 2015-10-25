from mongoengine import *

__all__ = ['Route']


class Route(Document):
    title = StringField(required=True)
    father = ObjectIdField(required=False)
    author = ObjectIdField(required=True)
    avg_rate = FloatField(required=True, default=0.0)
    n_rated = IntField(required=True, default=0)
    n_entered = IntField(required=True, default=0)
    n_completed = IntField(required=True, default=0)
    last_change_ts = IntField(required=False)
    create_ts = IntField(required=True)
    md_file = FileField(required=True)
    finished = BooleanField(required=True, default=False)
    n_attachment = IntField(required=True, default=0)
    attached = ListField(ObjectIdField())


class RateInfo(Document):
    user = ObjectIdField(required=True)
    route = ObjectIdField(required=True)
    score = IntField(required=True, choices=tuple(range(1,6)))

