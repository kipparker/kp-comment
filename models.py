from google.appengine.ext import ndb
from google.appengine.api import search

from comment_api_messages import CommentResponseMessage

TIME_FORMAT_STRING = '%Y-%m-%dT%H:%M:%S'
SEARCH_INDEX = 'api-comment'

def tokenize(str):
    a = []
    for word in str.split():
        j = 2
        while True:
            for i in range(len(word) - j + 1):
                a.append(word[i:i + j])
            if j == len(word):
                break
            j += 1
    return ','.join(a)

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
        comment = cls(content=request.content)
        comment.put()
        return comment

    def _post_put_hook(self, future):
        if self.content == "":
            self.content = "Nothing will come of nothing"
        doc = search.Document(
            doc_id='%s' % self.key.id(),
            fields=[
                search.TextField(name='content', value=self.content)
            ]
        )
        search.Index(SEARCH_INDEX).put(doc)

    @classmethod
    def _post_delete_hook(cls, key, future):
        search.Index(SEARCH_INDEX).delete('%s' % key.id())
