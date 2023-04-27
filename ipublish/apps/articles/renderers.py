from ipublish.apps.core.renderers import IprofileJSONRenderer

class ArticleJsonRenderer(IprofileJSONRenderer):
    object_label='article'
    pagination_object_label = 'articles'
    pagination_count_label = 'articlesCount'