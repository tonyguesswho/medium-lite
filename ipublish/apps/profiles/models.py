from django.db import models
from ipublish.apps.core.models import AbstractTimeStampedModel

class Profile(AbstractTimeStampedModel):

    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE)

    bio = models.TextField(blank=True)

    image = models.URLField(blank=True)

    follows = models.ManyToManyField('self', related_name='followed_by',symmetrical=False)

    favorites = models.ManyToManyField("articles.Article", related_name='favorited_by')

    def __str__(self):
        return self.user.username

    def follow(self,profile):
        self.follows.add(profile)

    def unfollow(self, profile):
        self.follows.remove(profile)

    def is_following(self, profile):
        return self.follows.filter(pk=profile.pk).exists()


    def is_followed_by(self, profile):
        return self.followed_by.filter(pk=profile.pk).exists()

    def favorite(self, article):
        """Favorite `article` if we haven't already favorited it."""
        self.favorites.add(article)

    def unfavorite(self, article):
        """Unfavorite `article` if we've already favorited it."""
        self.favorites.remove(article)

    def has_favorited(self, article):
        """Returns True if we have favorited `article`; else False."""
        return self.favorites.filter(pk=article.pk).exists()