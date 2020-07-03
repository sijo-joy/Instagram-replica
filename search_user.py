import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb

from myuser import MyUser


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class SearchUser(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        template_values = {
            'current_user': current_user,
        }
        template = JINJA_ENVIRONMENT.get_template('search_user.html')
        self.response.write(template.render(template_values))

    def post(self):
        current_user = users.get_current_user()
        if self.request.get('button') == 'Search':


            name = self.request.get('name')
            user_list = MyUser.query()
            if name:
                # raise UserWarning("ssssssssssss")
                user_list = user_list.filter(MyUser.name == name)
            user_list = user_list.fetch(10)
            # raise UserWarning(user_list)
            template_values = {
                'users': user_list,
                'current_user': current_user,
            }
            template = JINJA_ENVIRONMENT.get_template('search_user.html')
            self.response.write(template.render(template_values))
