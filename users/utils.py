from django.conf import settings

from authy.api import AuthyApiClient

AUTHY_API = AuthyApiClient(settings.TWILIO_ACCOUNT_SECURITY_API_KEY)

def get_authy_client():
    return AUTHY_API