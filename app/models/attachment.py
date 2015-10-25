from mongoengine import *
from enum import Enum

__all__ = ['Attachment', 'AttachType']


class AttachType(Enum):
    DOUBAN = 1
    URL = 2
    TEXT = 3


class Attachment(Document):
    route = ObjectIdField(required=True)
    atype = IntField(required=True, default=0)
    info = StringField(required=True)
    n_complete = IntField(required=True, default=0)
    upvote_list = ListField(ObjectIdField())


