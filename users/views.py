from django.shortcuts import render
from rest_framework import authentication, generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from .serializers import *

from django.http import Http404

class EmergencyContactsListView(generics.ListCreateAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    queryset = models.CustomUser.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    """
    Given a phone number, creates a User with that phone number or begins the process of creating one.
    """
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TokenView(APIView):
    """
    Given a phone number, creates a User with that phone number or begins the process of creating one.
    """
    def post(self, request, format=None):
        serializer = TokenSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            msg = serializer.save() # did the verification succeed?
            print(msg)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListCreateAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)
    queryset = models.CustomUser.objects.all()
    serializer_class = UserSerializer