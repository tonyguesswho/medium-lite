from ipublish.apps.core.renderers import IprofileJSONRenderer

class CommentJsonRenderer(IprofileJSONRenderer):
    object_label='comment'
    pagination_object_label = 'comments'
    pagination_count_label = 'commentsCount'