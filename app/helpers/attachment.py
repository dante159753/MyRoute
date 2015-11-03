import requests
import json
from bson import ObjectId
from flask.ext.login import current_user

from app.models.attachment import Attachment, AttachType
from app.app import app


class AttachmentHelper(object):
    @staticmethod
    def get(attach_id):
        return Attachment.objects(id=attach_id).first()

    @staticmethod
    def get_all():
        return Attachment.objects()

    @staticmethod
    def add(route_id, attach_type, key):
        from app.helpers.route import RouteHelper

        assert isinstance(route_id, ObjectId)
        assert RouteHelper.get(route_id)
        assert isinstance(attach_type, AttachType)

        # get book's info by isbn from douban
        if attach_type == AttachType.DOUBAN:
            r = requests.get(app.config['DOUBAN_ISBN_API'] + key)
            info = r.text
        elif attach_type == AttachType.URL:
            req_paras = {
                'url': key,
                'key': app.config['EMBEDLY_KEY']
            }
            r = requests.get(app.config['EMBEDLY_EXTRACT_API'], params=req_paras)

            json_info = json.loads(r.text)
            if json_info['type'] == 'error':
                return

            info = r.text
        else:
            info = key

        new_attach = Attachment()
        new_attach.route = route_id
        new_attach.atype = attach_type.value
        new_attach.info = info
        new_attach.save()

        f_route = RouteHelper.get(route_id)
        f_route.attached.append(new_attach.id)
        f_route.save()

        return new_attach

    @staticmethod
    def delete(attach_id):
        from app.helpers.route import RouteHelper

        assert isinstance(attach_id, ObjectId)
        assert AttachmentHelper.get(attach_id)

        attach = AttachmentHelper.get(attach_id)
        f_route = RouteHelper.get(attach.route)
        f_route.attached.remove(attach_id)
        f_route.save()
        attach.delete()

    @staticmethod
    def toggle_vote(attach_id):
        assert isinstance(attach_id, ObjectId)
        assert AttachmentHelper.get(attach_id)

        attach = AttachmentHelper.get(attach_id)
        if current_user.id not in attach.upvote_list:
            attach.upvote_list.append(current_user.id)
            attach.save()
            return 'upvote', len(attach.upvote_list)
        if current_user.id in attach.upvote_list:
            attach.upvote_list.remove(current_user.id)
            attach.save()
            return 'downvote', len(attach.upvote_list)

    @staticmethod
    def get_n_upvote(attach_id):
        assert isinstance(attach_id, ObjectId)
        assert AttachmentHelper.get(attach_id)

        attach = AttachmentHelper.get(attach_id)

        return len(attach.upvote_list)

