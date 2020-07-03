import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from google.appengine.ext import blobstore
from myuser import MyUser
from datetime import datetime
from uploadhandler import UploadHandler
from downloadhandler import DownloadHandler
from blobcollection import BlobCollection
from user_profile import UserProfile
from search_user import SearchUser
from list_users import ListUsers
from comments import Comments


JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True
)



class MainPage(webapp2.RequestHandler):
	def get(self):
		show_all_key = ''
		if self.request.get('show_all_key'):
			show_all_key = ndb.Key(urlsafe=self.request.get('show_all_key'))
		self.response.headers['Content-Type'] = 'text/html'

		url = ''
		url_string = ''
		post = ''

		welcome = 'Welcome back'
		myuser = None
		posts = []
		comment_dictonary = {}
		user = users.get_current_user()
		if user:
			url = users.create_logout_url(self.request.uri)
			url_string = 'logout'
			myuser_key = ndb.Key('MyUser', user.user_id())
			myuser = myuser_key.get()

			post = BlobCollection.query().order(-BlobCollection.posted_date).fetch(limit=50)
			if myuser == None:
				welcome = 'Welcome to the Instagram'
				myuser = MyUser(id=user.user_id())
				myuser.name = user.email()
				myuser.put()
			key_list = []
			if myuser:
				for follo in myuser.following:
					use = MyUser.query().filter(MyUser.name == follo)
					use = use.fetch(10)
					for ussss in use:
						key_list.append(ussss.key)
				# raise UserWarning(key_list)
				for p in post:
					if p.user_key == myuser.key or p.user_key in key_list:
						posts.append(p)
				for pst in posts:
					comments = Comments.query().filter(Comments.post_key == pst.key).order(-Comments.posted_date)
					comment_dictonary[pst.key] = comments

		else:
			url = users.create_login_url(self.request.uri)
			url_string = 'login'
		# raise UserWarning(posts)
		template_values = {
			'url' : url,
			'show_all_key' : show_all_key,
			'posts': posts,
			'comment_dictonary': comment_dictonary,
			'upload_url': blobstore.create_upload_url('/upload'),
			'url_string' : url_string,
			'user' : user,
			'welcome' : welcome,
			'myuser' : myuser
		}

		template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(template.render(template_values))
	def post(self):
		logged_user = users.get_current_user()
		logged_user = ndb.Key('MyUser', logged_user.user_id())
		logged_user = logged_user.get()
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
			self.redirect('/')


app = webapp2.WSGIApplication([
	('/', MainPage),
	('/upload', UploadHandler),
	('/list_users', ListUsers),
	('/download', DownloadHandler),
	('/user_profile', UserProfile),
	('/search_user', SearchUser),
], debug=True)
