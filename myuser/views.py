from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.views import APIView, Response, status
from . import serializers
User = get_user_model()


class UserUpdateView(APIView):

    def get(self, request, pk):

        person = User.objects.filter(user=pk).first()
        serializer = serializers.UserDetailSerializer(person, context={'request': request})

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request, pk):

        admin = User.objects.filter(pk=request.user.id).first()
        person = User.objects.filter(pk=pk).first()

        if admin != person:
            return Response('error: You can change only yours data', status.HTTP_403_FORBIDDEN)

        serializer = serializers.UserUpdateSerializer(admin, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_205_RESET_CONTENT)

        return Response(status.HTTP_400_BAD_REQUEST)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserCreateSerializer





