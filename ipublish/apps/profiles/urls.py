from django.urls import path
from .views import ProfileRetrieveView, ProfileFollowApiView

app_name='profiles'

urlpatterns = [
    path('profiles/<str:username>', ProfileRetrieveView.as_view()),
     path(
       'profiles/<str:username>/follow', ProfileFollowApiView.as_view()
      ),
]
