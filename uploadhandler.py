from google.appengine.ext import blobstore
from blobcollection import BlobCollection
from google.appengine.ext import ndb
from google.appengine.api import users
from datetime import datetime
from google.appengine.ext.webapp import blobstore_handlers

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload = self.get_uploads()[0]
        caption = self.request.get('caption')
        current_user = users.get_current_user()
        current_user = ndb.Key('MyUser', current_user.user_id())
        current_user = current_user.get()
        post = BlobCollection()
        post.caption = caption
        now = datetime.now()
        post.posted_date = now
        post.user_key = current_user.key
        post.blob_key = upload.key()
        post.put()
        self.redirect('/')