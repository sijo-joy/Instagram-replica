from google.appengine.ext import ndb
from blobcollection import BlobCollection
from myuser import MyUser
class Comments(ndb.Model):
    post_key = ndb.KeyProperty(BlobCollection)
    user_key = ndb.StringProperty()
    comment = ndb.StringProperty()
    posted_date = ndb.DateTimeProperty()