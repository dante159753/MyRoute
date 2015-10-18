from mongoengine import *

__all__ = ['EnteredRoute', 'CompleteInfo']


class CompleteInfo(EmbeddedDocument):
    attach = ObjectIdField(required=True)
    finished = BooleanField(required=True, default=False)


class EnteredRoute(Document):
    user = ObjectIdField(required=True)
    route = ObjectIdField(required=True)
    percentage = IntField(default=0)
    attach_complete = ListField(EmbeddedDocumentField(CompleteInfo))


