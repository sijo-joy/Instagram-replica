import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class ListUsers(webapp2.RequestHandler):
    def get(self):
        logged_user = users.get_current_user()
        user_key = ndb.Key(urlsafe=self.request.get('user_key'))
        profile_user_obj = user_key.get()
        view = self.request.get('view')
        users_list = []
        if view == 'followers':
            users_list = profile_user_obj.followers
        elif view == 'following':
            users_list = profile_user_obj.following
        template_values = {

            'logged_user': logged_user,
            'users_list': users_list,
        }

        template = JINJA_ENVIRONMENT.get_template('list_users.html')
        self.response.write(template.render(template_values))