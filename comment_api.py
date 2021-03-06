"""Simple API with get, list, write and search methods for comments"""

import endpoints
from protorpc import remote
from protorpc import message_types
from models import Comment, SEARCH_INDEX
from comment_api_messages import CommentResponseMessage, CommentListResponse, CommentRequestMessage
from google.appengine.api import search
from google.appengine.ext import ndb

WEB_CLIENT_ID = '526127305693-d0r6fc60sc58olunmh71upmaudk4errm.apps.googleusercontent.com'
ANDROID_AUDIENCE = WEB_CLIENT_ID

@endpoints.api(
    name='comments',
    version='v1',
    description="Comments API",
    allowed_client_ids=[WEB_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
    audiences=[ANDROID_AUDIENCE],
    scopes=[endpoints.EMAIL_SCOPE],
    auth_level=endpoints.AUTH_LEVEL.REQUIRED
)
class CommentApi(remote.Service):
    @endpoints.method(CommentRequestMessage, CommentListResponse,
                      path='comment/search', http_method='GET',
                      name='comment.search')
    def comment_search(self, request):
        """
        Arguments:
            CommentRequestMessage, with content used for search

        Returns:
            An instance of CommentListResponse.
        """
        term = request.content or ""
        comment_search = search.Index(SEARCH_INDEX).search(term)
        comment_keys = [ndb.Key(Comment, int(x.doc_id)) for x in comment_search.results]
        q = Comment.query().filter(Comment._key.IN(comment_keys))
        items = [entity.to_message() for entity in q.iter()]
        return CommentListResponse(items=items)

    @endpoints.method(message_types.VoidMessage, CommentListResponse,
                      path='comment', http_method='GET',
                      name='comment.list')
    def comment_list(self, request):
        """
        Returns:
            An instance of CommentListResponse.
        """
        items = [entity.to_message() for entity in Comment.query()]
        return CommentListResponse(items=items)

    @endpoints.method(CommentRequestMessage, CommentResponseMessage,
                      path='comment', http_method='POST',
                      name='comment.add')
    def comment_add(self, request):
        """API endpoint to add a comment
        """
        comment = Comment.put_from_message(request)
        return comment.to_message()

APPLICATION = endpoints.api_server([CommentApi])
