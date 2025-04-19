from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
    ListAPIView,
    RetrieveAPIView,
)

from users.serializers import UserRegisterSerializer, UserSerializer

USER = get_user_model()


class UserRegisterView(CreateAPIView):
    queryset = USER.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        self.check_object_permissions(self.request, self.request.user)
        return self.request.user
