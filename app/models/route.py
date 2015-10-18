from mongoengine import *

__all__ = ['Route']


class Route(Document):
    father = ObjectIdField(required=True)
    rate = FloatField(required=True, default=0.0)
    n_rate = IntField(required=True, default=0)
    n_entered = IntField(required=True, default=0)
    md_file = StringField(required=True)
    attached = ListField(ObjectIdField())


