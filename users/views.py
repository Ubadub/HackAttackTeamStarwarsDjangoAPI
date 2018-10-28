from django.shortcuts import render
from rest_framework import authentication, generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from .serializers import *

from django.http import Http404

class EmergencyContactsView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.CustomUser.objects.all()
    serializer_class = UserSerializer

    def post(self, request, format=None):
        serializer = TokenSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            msg = serializer.save() # did the verification succeed?
            print(msg)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """
    Given a phone number, creates a `User` with that phone number, and then sends a text with a confirmation code.
    The `User` is **NOT** active (i.e. they can't do anything) until they get an authorization token, which is done
    via the next API endpoint.
    """
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TokenView(APIView):
    """
    Given a phone number and four-digit verification token (sent via text message),
    checks if the verification token is valid for the given phone number. If it is,
    it activates the `User` account and returns an authentication token to be used
    in all future API requests.
    """
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = TokenSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            msg = serializer.save() # did the verification succeed?
            print(msg)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListCreateAPIView):
    http_method_names = ['get', 'options']
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = (permissions.IsAdminUser,)
    queryset = models.CustomUser.objects.all()
    serializer_class = UserSerializer