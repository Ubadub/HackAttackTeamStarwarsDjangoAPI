from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'password', 'phone_number', 'groups')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user