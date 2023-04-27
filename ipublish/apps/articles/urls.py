from django.urls import include, path

from rest_framework.routers import DefaultRouter
from .views import ArticleViewset, ArticlesFavoriteAPIView, TagListAPIView,  ArticlesFeedAPIView
from  ipublish.apps.comments.views import CommentsListCreateAPIView, DestroyCommentApiView

router = DefaultRouter(trailing_slash=False)


router.register(r'articles', ArticleViewset)
app_name = 'articles'

urlpatterns = [
    path('', include(router.urls)),
    path(
       'articles/<slug:article_slug>/comments',
       CommentsListCreateAPIView.as_view()
      ),
    path(
       'articles/<slug:article_slug>/comments/<int:comment_pk>',
       DestroyCommentApiView.as_view()
      ),
     path(
       'articles/<slug:article_slug>/favorite',
       ArticlesFavoriteAPIView.as_view()
      ),
    path('tags', TagListAPIView.as_view()),
    path('articles/feed', ArticlesFeedAPIView.as_view()),
]
