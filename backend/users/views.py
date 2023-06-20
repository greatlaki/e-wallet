from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from django.contrib.auth import logout

from users.serializers import RegisterSerializer, LoginSerializer


class RegisterApiView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()


class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()


class LogoutAPIView(APIView):
    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
