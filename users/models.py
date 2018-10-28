from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.authtoken.models import Token

from .managers import UserManager
from .utils import get_authy_client

PHONE_REGEX = r"^\+?1?\d{9,15}$"
TWILIO_VIA_SMS = 'sms'

class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex=PHONE_REGEX,
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    phone_number = models.CharField(_('phone number'), unique=True, validators=[phone_regex], max_length=17,
        blank=False)
    first_name = models.CharField(_('first name'), max_length=50, blank=False)
    last_name = models.CharField(_('last name'), max_length=50, blank=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=False)
    emergency_contacts = models.ManyToManyField('self', related_name='protectees', related_query_name='protectors')
    #avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_admin = models.BooleanField(default=False)


    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name'] # USERNAME_FIELD and password included by default

    @property
    def is_staff(self):
        return self.is_admin

    def send_verification_text(self, country_code=settings.TWILIO_US_COUNTRY_CODE):
        """
        Sends a verification text (if not in DEBUG mode).

        Presently uses the US' country code by default.
        """
        if not settings.DEBUG:
            get_authy_client().phones.verification_start(
                self.phone_number,
                country_code,
                via=TWILIO_VIA_SMS
                )
        else:
            print("DEBUG MODE ON; NO VERIFICATION MESSAGE SENT")

    def validate_verification_text(self, token, country_code=settings.TWILIO_US_COUNTRY_CODE):
        """
        Confirms that a verification code against the message that was actually
        sent by `send_verification_text()`

        Presently uses the US' country code by default.
        """
        verification = None

        if not settings.DEBUG:
            verification = authy_api.phones.verification_check(
                self.phone_number,
                country_code,
                token
            )

        if settings.DEBUG or verification.ok():
            self.is_active = True
            self.save()
            t = Token.objects.create(user=self)
            return {'status_code' : status.HTTP_200_OK, 'auth_token' : t.key}

        else:
            d = {'status_code' : status.HTTP_401_UNAUTHORIZED, 'errors':[]}
            for error_msg in verification.errors().values():
                if error_msg.lower() != 'error':
                    d['errors'].append(error_msg)

            return d

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def add_emergency_contact(self, contact):
        pass

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

