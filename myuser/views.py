from rest_framework import generics
from django.contrib.auth import get_user_model
from . import serializers
from rest_framework.permissions import IsAuthenticated
User = get_user_model()


class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = serializers.UserDetailSerializer


class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = serializers.UserUpdateSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserCreateSerializer





