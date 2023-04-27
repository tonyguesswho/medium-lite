from django.apps import AppConfig


class ArticlesAppConfig(AppConfig):
    name = 'ipublish.apps.articles'
    label = 'articles'
    verbose_name = 'Articles'

    def ready(self):
        import ipublish.apps.articles.signals

default_app_config = 'ipublish.apps.articles.ArticlesAppConfig'