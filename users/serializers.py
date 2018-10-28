from django.conf import settings

from rest_framework import serializers
from rest_framework import status
from .models import CustomUser

from users.models import PHONE_REGEX

class EmergencyContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'first_name', 'last_name')

class LoginSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50, allow_blank=False)
    last_name = serializers.CharField(max_length=50, allow_blank=False)
    phone_number = serializers.RegexField(PHONE_REGEX, max_length=17, allow_blank=False)

    def create(self, validated_data):
        """
        Creates a `CustomUser` with the given data and sends a confirmation text.
        """
        phone_number = validated_data['phone_number']
        user = None
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            user.invalidate_token()
        except CustomUser.DoesNotExist as e:
            user = CustomUser.objects.create(**validated_data)
        
        user.send_verification_text()
        return user

class TokenSerializer(serializers.Serializer):
    phone_number = serializers.RegexField(PHONE_REGEX, max_length=17, allow_blank=False)
    auth_token = serializers.CharField(min_length=settings.TWILIO_TOKEN_LENGTH,
        max_length=settings.TWILIO_TOKEN_LENGTH, allow_blank=False)

    def validate(self, attrs):
        print(attrs)
        phone_number = attrs.get('phone_number')
        auth_token = attrs.get('auth_token')

        print("phone number and auth token are {0} and {1}".format(phone_number, auth_token))
        if phone_number and auth_token:
            try:
                user = CustomUser.objects.get(phone_number=phone_number)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError('Invalid phone number.', code='authorization')

            else:
                validation_response = user.validate_verification_text(token=auth_token)
                print(validation_response)

                if validation_response['status_code'] != status.HTTP_200_OK:
                    raise serializers.ValidationError(validation_response['errors'], code='invalid_auth_token')

                else:
                    attrs['auth_token'] = validation_response['auth_token']

        else:
            msg = 'Must include "phone number" and "auth_token".'
            raise serializers.ValidationError(msg, code='authorization')

        return attrs

    def create(self, validated_data):
        """
        Returns the appropriate `Token` (which was generated during validation)with the given data and sends a confirmation text.
        """
        auth_token = validated_data['auth_token']
        return CustomUser.objects.get(auth_token=auth_token)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'first_name', 'last_name')