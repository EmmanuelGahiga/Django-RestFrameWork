from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import generics, status
from rest_framework.views import APIView
from .serializers import SignUpSerializer
from .tokens import create_jwt_pair_for_user
from rest_framework.permissions import AllowAny

# Create your views here.


class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            tokens = create_jwt_pair_for_user(user)

            response = {"message": "SignIn successifully", "tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(
            data={"message": "Envalid email or password"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}
        return Response(data=content, status=status.HTTP_200_OK)
