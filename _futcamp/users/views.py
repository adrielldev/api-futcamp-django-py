from rest_framework import generics
from rest_framework.views import APIView, Response, Request, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from utils import IsAdmin, IsOwner
from .serializers import (
    UserSerializer,
    UserDetailSerializer,
    UserEnableDisableSerializer,
)
from .serializers import Loginserializer
from .models import User


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin | IsOwner]

    serializer_class = UserDetailSerializer
    queryset = User.objects.all()

    lookup_url_kwarg = "user_id"


class EnableDisableUserView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    serializer_class = UserEnableDisableSerializer
    queryset = User.objects.all()

    lookup_url_kwarg = "user_id"


class loginView(APIView):
    def post(self, request: Request):
        serializer = Loginserializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if not user:
            return Response(
                {"detail": "invalid credentials"}, status.HTTP_403_FORBIDDEN
            )
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})


class updateView(generics.UpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    serializer_class = UserEnableDisableSerializer
    queryset = User.objects.all()

    lookup_url_kwarg = "user_id"
