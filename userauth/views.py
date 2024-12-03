from django.shortcuts import render
from rest_framework import generics, status
from registeration.models import Attendee
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from userauth.serializers import LoginSerializer


class AttendeeLogin(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        attendee = Attendee.objects.filter(cys_code=username).first()
        if attendee:
            auth_user = User.objects.filter(username=username).first()

            if auth_user and auth_user.check_password(password):
                refresh = RefreshToken.for_user(auth_user)
                return Response(
                    {
                        "status": "success",
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "status": "error",
                    "message": "Invalid credentials",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"status": "error", "message": "User does not exist"},
            status=status.HTTP_404_NOT_FOUND,
        )
