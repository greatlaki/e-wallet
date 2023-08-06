from django.contrib.auth import logout
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from users.serializers import LoginSerializer, RegisterSerializer


class RegisterApiView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        user = super().post(request, *args, **kwargs)
        return Response(user.data, status=status.HTTP_201_CREATED)


class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        logout(request)
        return Response({"success": "Successfully logged out"}, status=status.HTTP_200_OK)
