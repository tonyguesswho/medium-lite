from django.db import models
from ipublish.apps.core.models import AbstractTimeStampedModel

class Comment(AbstractTimeStampedModel):
    body = models.TextField()

    article = models.ForeignKey("articles.Article", related_name='comments', on_delete=models.CASCADE)

    author = models.ForeignKey("profiles.Profile", related_name='comments', on_delete=models.CASCADE)