from mongoengine import *

__all__ = ['Attachment']


class Attachment(Document):
    route = ObjectIdField(required=True)
    atype = IntField(required=True, default=0)
    key = StringField(required=True)
    rate = FloatField(required=True, default=0.0)
    n_rate = IntField(required=True, default=0)
    n_complete = IntField(required=True, default=0)


