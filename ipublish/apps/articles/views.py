from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework import generics

from .models import Article, Tag
from .serializers import ArticleSerializer, TagSerializer
from .renderers import ArticleJsonRenderer


class ArticleViewset(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    lookup_field = 'slug'
    queryset = Article.objects.select_related('author', 'author__user')
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticleJsonRenderer,)
    serializer_class = ArticleSerializer

    def get_queryset(self):
        queryset = self.queryset

        author = self.request.query_params.get('author', None)
        if author is not None:
            queryset = queryset.filter(author__user__username=author)

        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            queryset = queryset.filter(tags__tag=tag)

        favorited_by = self.request.query_params.get('favorited', None)
        if favorited_by is not None:
            queryset = queryset.filter(
                favorited_by__user__username=favorited_by
            )

        return queryset

    def create(self, request, *args, **kwargs):
        serializer_context = {
            'author': request.user.profile,
            'request': request
        }
        serializer_data = request.data.get('article', {})

        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer_context = {'request': request}

        page = self.paginate_queryset(self.get_queryset())

        serializer = self.serializer_class(
            page,
            context=serializer_context,
            many=True
        )

        return self.get_paginated_response(serializer.data)

    def update(self, request, slug):
        serializer_context = {'request': request}
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')

        serializer_data = request.data.get('article', {})

        serializer = self.serializer_class(
            serializer_instance, data=serializer_data, context=serializer_context, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, slug):
        serializer_context ={
            'request':request
        }
        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')
        serializer = self.serializer_class(serializer_instance, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ArticlesFavoriteAPIView(APIView):
        permission_classes = (IsAuthenticated,)
        renderer_classes = ( ArticleJsonRenderer,)
        serializer_class = ArticleSerializer

        def delete(self, request, article_slug=None):
            profile = self.request.user.profile
            serializer_context = {'request': request}

            try:
                article = Article.objects.get(slug=article_slug)
            except Article.DoesNotExist:
                raise NotFound('An article with this slug was not found.')

            profile.unfavorite(article)

            serializer = self.serializer_class(article, context=serializer_context)

            return Response(serializer.data, status=status.HTTP_200_OK)

        def post(self, request, article_slug=None):
            profile = self.request.user.profile
            serializer_context = {'request': request}

            try:
                article = Article.objects.get(slug=article_slug)
            except Article.DoesNotExist:
                raise NotFound('An article with this slug was not found.')

            profile.favorite(article)

            serializer = self.serializer_class(article, context=serializer_context)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    pagination_class = None
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer

    def list(self, request):
        serializer_data = self.get_queryset()
        serializer = self.serializer_class(serializer_data, many=True)

        return Response({
            'tags': serializer.data
        }, status=status.HTTP_200_OK)


class ArticlesFeedAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Article.objects.all()
    renderer_classes = (ArticleJsonRenderer,)
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.filter(
            author__in=self.request.user.profile.follows.all()
        )

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        serializer_context = {'request': request}
        serializer = self.serializer_class(
            page, context=serializer_context, many=True
        )

        return self.get_paginated_response(serializer.data)

