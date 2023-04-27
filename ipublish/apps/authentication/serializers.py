from rest_framework import  serializers
from .models import User
from ipublish.apps.profiles.serializers import ProfileSerializer

from django.contrib.auth import authenticate

class RegistrationSerilaizer(serializers.ModelSerializer):
    """Serilaizers registration request and creates user"""

    password = serializers.CharField(max_length = 128, min_length = 8, write_only = True)

    token = serializers.CharField(read_only=True, max_length=255)



    class Meta:
        model = User

        fields = ['email','username','token', 'password']

    def create(self, validated_data):
         return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):

    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields =  ['email', 'username', 'password', 'token']

    def validate(self, data):
         email = data.get('email', None)
         password = data.get('password', None)

         if email is None:
             raise serializers.ValidationError('Email not provided')

         if password is None:
             raise serializers.ValidationError('password not provided')

         user = authenticate(email=email, password=password)

         if user is None:
             raise serializers.ValidationError('user does not exist')

         if not user.is_active:
            raise serializers.ValidationError('User has been deactivated')

         return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    profile = ProfileSerializer(write_only=True)

    bio = serializers.CharField(source='profile.bio', read_only=True)
    image = serializers.CharField(source='profile.image', read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token', 'profile', 'bio', 'image',)
        read_only_fields = ('token',)


    def update(self, instance, validated_data):
        """Performs an update on a User."""
        password = validated_data.pop('password', None)

        profile_data = validated_data.pop('profile', {})

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)
        instance.save()

        for (key, value) in profile_data.items():
            setattr(instance.profile, key, value)
        instance.profile.save()

        return instance