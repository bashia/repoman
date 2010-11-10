import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from repository.lib.base import BaseController

# custom imports

from repository.model import meta
from repository.model.user import User
from repository.model.group import Group
from repository.model.form import validate_new_user, validate_modify_user
from repository.lib import helpers as h
from repository.lib.authorization import authorize, AllOf, AnyOf, NoneOf, HasPermission
from repository.lib import beautify

from pylons import app_globals

import formencode
###

log = logging.getLogger(__name__)

def auth_403(message):
    abort(403, "403 Forbidden : '%s'" % message)


class UsersController(BaseController):

    def list_all(self, format='json'):
        user_q = meta.Session.query(User).filter(User.deleted!=True)
        users = [user.user_name for user in user_q]
        urls = [url('user', user=u, qualified=True) for u in users]
        if format == 'json':
            response.headers['content-type'] = app_globals.json_content_type
            return h.render_json(urls)
        else:
            abort(501, '501 Not Implemented')

    def new_user(self, format='json'):
        params = validate_new_user(request.params)
        new_user = User(cert_dn=params['cert_dn'],
                        user_name=params['user_name'],
                        email=params['email'])
        new_user.full_name = params['full_name']
        new_user.suspended = params['suspended']

        # Deal with user groups
        groups = params['groups']
        if not groups:
            groups = [app_globals.default_user_group]
        else:
            groups = groups.rstrip(',').split(',')
            # Check for default user group
            if 'users' not in groups:
                groups.append(app_globals.default_user_group)

        # Do group membership
        #TODO: change from group name to group uuid for membership?
        group_q = meta.Session.query(Group)
        groups = [group_q.filter(Group.name==g).first() for g in groups]
        if None in groups:
            # abort if any specified group does not exist
            abort(400, '400 Bad Request')
        else:
            [new_user.groups.append(g) for g in groups]

        # Update the database
        meta.Session.add(new_user)
        meta.Session.commit()
        return h.render_json(beautify.user(new_user))

    def modify_user(self, user, format='json'):
        params = validate_modify_user(request.params)

        user_q = meta.Session.query(User)
        user = user_q.filter(User.user_name==user).first()

        if user:
            for k,v in params.iteritems():
                if v:
                    setattr(user, k, v)
            meta.Session.commit()
        else:
            abort(404, '404 Not Found')

    def delete_user(self, user, format='json'):
        user = meta.Session.query(User).filter(User.user_name==user).first()
        if user:
            # do something better here
            user.deleted = True
        else:
            abort(404, '404 Not Found')

    def show(self, user, format='json'):
        user = meta.Session.query(User).filter(User.user_name==user).first()
        if user:
            if format=='json':
                response.headers['content-type'] = app_globals.json_content_type
                return h.render_json(beautify.user(user))
            else:
                abort(501, '501 Not Implemented')
        else:
            abort(404, '404 Not Found')

    def list_images(self, user, format='json'):
        user = meta.Session.query(User).filter(User.user_name==user).first()
        if user:
            images = user.images
            images_repr = representation.image_repr(*images)
            if format=='json':
                response.headers['content-type'] = app_globals.json_content_type
                return h.render_json(images_repr)
            else:
                abort(501, '501 Not Implemented')
        else:
            abort(404, '404 Not Found')

    def list_groups(self, user, format='json'):
        return url('group', group='test', qualified=True)
        user = meta.Session.query(User).filter(User.user_name==user).first()
        if user:
            groups = user.groups
            groups_repr = representation.group_repr(*groups)
            if format=='json':
                response.headers['content-type'] = app_globals.json_content_type
                return h.render_json(groups_repr)
            else:
                abort(501, '501 Not Implemented')
        else:
            abort(404, '404 Not Found')

    def list_shared_images(self, user, format='json'):
        pass

