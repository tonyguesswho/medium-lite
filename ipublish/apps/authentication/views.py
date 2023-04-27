from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated


from .serializers import  (
    RegistrationSerilaizer,  LoginSerializer, UserSerializer
)
from .renderers import  UserJSONRenderer

class RegistrationView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerilaizer
    renderer_classes = (UserJSONRenderer,)


    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)



class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception = True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class  UserRetrieveUpdateApiView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    renderer_classes = (UserJSONRenderer,)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})

        serializer_data = {
           'username': user_data.get('username', request.user.username),
           'email': user_data.get('email', request.user.email),
           'profile': {
               'bio': user_data.get('bio', request.user.profile.bio),
               'image': user_data.get('image', request.user.profile.image)
             }
        }


        serializer = self.serializer_class(request.user, data=serializer_data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)




