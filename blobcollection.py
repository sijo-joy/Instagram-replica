from google.appengine.ext import ndb
from myuser import MyUser
class BlobCollection(ndb.Model):
    blob_key = ndb.BlobKeyProperty()
    caption = ndb.StringProperty()
    user_key = ndb.KeyProperty(MyUser)
    posted_date = ndb.DateTimeProperty()
