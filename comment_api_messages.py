from protorpc import messages

class CommentResponseMessage(messages.Message):
    """Return a comment"""
    id = messages.IntegerField(1)
    comment = messages.StringField(2)
    added = messages.StringField(3)

class CommentListResponse(messages.Message):
    """ProtoRPC message definition to represent a list of stored scores."""
    items = messages.MessageField(CommentResponseMessage, 1, repeated=True)

class CommentRequestMessage(messages.Message):
    """incoming content"""
    content = messages.StringField(1)
