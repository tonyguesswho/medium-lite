from django.urls import path
from .views import RegistrationView, LoginView, UserRetrieveUpdateApiView


app_name = 'authentication'

urlpatterns = [
    path('user/', UserRetrieveUpdateApiView.as_view()),
    path('users/', RegistrationView.as_view()),
    path('users/login/', LoginView.as_view())
]
