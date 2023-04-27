from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import serializers

from .models import Profile
from .renderers import ProfileJsonRenderer
from .serializers import ProfileSerializer
from .exceptions import  ProfileDoesNotExist

class ProfileRetrieveView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Profile.objects.select_related('user')
    serializer_class = ProfileSerializer
    renderer_classes =(ProfileJsonRenderer,)


    def retrieve(self, request, username, *args, **kwargs):
        try:
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound('A profile with this username does not exist.')

        serializer= self.serializer_class(profile, context={'request':request})

        return Response(serializer.data, status=status.HTTP_200_OK)




class  ProfileFollowApiView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJsonRenderer,)
    serializer_class = ProfileSerializer


    def delete(self, request, username=None):
        follower = self.request.user.profile

        try:
            followee = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound('A profile with this username was not found.')

        follower.unfollow(followee)

        serializer = self.serializer_class(followee, context={
            'request': request
        })

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, username=None):
        follower = self.request.user.profile

        try:
            followee = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound('A profile with this username was not found.')

        if follower.pk is followee.pk:
            raise serializers.ValidationError('You can not follow yourself.')

        follower.follow(followee)

        serializer = self.serializer_class(followee, context={
            'request': request
        })

        return Response(serializer.data, status=status.HTTP_201_CREATED)
