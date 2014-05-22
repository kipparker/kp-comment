"""Simple API with get, list, write and search methods for comments"""

import endpoints
from protorpc import remote
from protorpc import message_types
from models import Comment, comment_key
from comment_api_messages import CommentResponseMessage, CommentListResponse, CommentAddMessage



@endpoints.api(name='comments', version='v1', description="Comments API")
class CommentApi(remote.Service):
    @endpoints.method(message_types.VoidMessage, CommentListResponse,
                      path='comment', http_method='GET',
                      name='comment.list')
    def comment_list(self, request):
        """
        Returns:
            An instance of CommentListResponse. If the request contains q, will
            only return matching comments
        """
        items = [entity.to_message() for entity in Comment.query()]
        return CommentListResponse(items=items)

    @endpoints.method(CommentAddMessage, CommentResponseMessage,
                      path='comment', http_method='POST',
                      name='comment.add')
    def comment_add(self, request):
        """API endpoint to add a comment
        """
        comment = Comment.put_from_message(request)
        return comment.to_message()

APPLICATION = endpoints.api_server([CommentApi])
