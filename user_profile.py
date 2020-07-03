import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from google.appengine.ext import blobstore
from myuser import MyUser
from comments import Comments
from datetime import datetime
from blobcollection import BlobCollection

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class UserProfile(webapp2.RequestHandler):
    def get(self):
        comment_dictonary = {}
        show_all_key = ''
        if self.request.get('show_all_key'):
            show_all_key = ndb.Key(urlsafe=self.request.get('show_all_key'))
        user_key = ndb.Key(urlsafe=self.request.get('user_key'))
        profile_user_obj = user_key.get()
        logged_user = users.get_current_user()
        logged_user = ndb.Key('MyUser', logged_user.user_id())
        logged_user = logged_user.get()
        is_following = False
        if profile_user_obj != logged_user:
            if profile_user_obj.name in logged_user.following:
                is_following = True
        posts = BlobCollection.query().filter(BlobCollection.user_key == user_key).order(-BlobCollection.posted_date)
        for pst in posts:
            comments = Comments.query().filter(Comments.post_key == pst.key).order(-Comments.posted_date)
            comment_dictonary[pst.key] = comments
        # len_post = 0
        # for p in posts:
        #

        len_followers = len(profile_user_obj.followers)
        len_following = len(profile_user_obj.following)
        len_posts = 0
        for p in posts:
            len_posts += 1
        template_values = {
            'len_posts': len_posts,
            'show_all_key': show_all_key,
            'len_followers': len_followers,
            'comment_dictonary': comment_dictonary,
            'profile_user_obj': profile_user_obj,
            'len_following': len_following,
            'logged_user': logged_user,
            'posts': posts,
            'user_key': user_key.urlsafe(),
            'is_following': is_following,

        }

        template = JINJA_ENVIRONMENT.get_template('user_profile.html')
        self.response.write(template.render(template_values))
    def post(self):
        user_key = ndb.Key(urlsafe=self.request.get('user_key'))
        profile_user_obj = user_key.get()
        logged_user = users.get_current_user()
        logged_user = ndb.Key('MyUser', logged_user.user_id())
        logged_user = logged_user.get()
        if self.request.get('button') == "Follow":
            logged_user.following.append(str(profile_user_obj.name))
            logged_user.put()
            profile_user_obj.followers.append(str(logged_user.name))
            profile_user_obj.put()
            self.redirect('/')
        if self.request.get('button') == "Unfollow":
            logged_user.following.remove(str(profile_user_obj.name))
            logged_user.put()
            profile_user_obj.followers.remove(str(logged_user.name))
            profile_user_obj.put()
            self.redirect('/')
        if self.request.get('button') == "comment":
            post_key = ndb.Key(urlsafe=self.request.get('post'))
            post = post_key.get()
            comment = self.request.get('comment')
            if comment:
                comment_id = Comments()
                now = datetime.now()
                comment_id.posted_date = now
                comment_id.post_key = post_key
                comment_id.user_key = logged_user.name
                comment_id.comment = comment
                comment_id.put()
            self.redirect('/user_profile?user_key=%s' % user_key.urlsafe())




