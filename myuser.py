from google.appengine.ext import ndb

class MyUser(ndb.Model):
	name = ndb.StringProperty()
	followers = ndb.StringProperty(repeated=True)
	following = ndb.StringProperty(repeated=True)