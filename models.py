from google.appengine.ext import ndb

from comment_api_messages import CommentResponseMessage

TIME_FORMAT_STRING = '%Y-%m-%dT%H:%M:%S'


def comment_key(comment_on='homepage'):
    """Constructs a Datastore key for a Comment entity with comment_on."""
    return ndb.Key('Comment', comment_on)

class Comment(ndb.Model):
    """Text message and date."""
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    @property
    def timestamp(self):
        """Property to format a datetime object to string."""
        return self.date.strftime(TIME_FORMAT_STRING)

    def to_message(self):
        """Turns the Comment entity into a ProtoRPC object.
        """
        return CommentResponseMessage(id=self.key.id(),
                                    comment=self.content,
                                    added=self.timestamp)

    @classmethod
    def put_from_message(cls, request):
        comment = cls(parent=comment_key(), content=request.content)
        comment.put()
        return comment
