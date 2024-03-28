from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'image')


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'image')


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'name', 'image', 'password')