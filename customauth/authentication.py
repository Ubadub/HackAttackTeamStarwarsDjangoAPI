# my_app/authentication.py
from .models import User
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.authtoken.models import Token

# class CustomAuthBackend(authentication.BaseAuthentication):

#     def authenticate(self, phone, password):
#         return self.get_user(phone, password)

#     def get_user(self, phone, password):
#         try:
#             user = User.objects.get(phone=phone)
#             if user.check_password(password):
#                 return user
#         except User.DoesNotExist:
#             # exception handling
#             return None
#         return None

# class CustomAuthBackend(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         username = request.META.get('X_USERNAME') # get the username request header
#         if not username: # no username passed in request headers
#             return None # authentication did not succeed

#         try:
#             user = User.objects.get(username=username) # get the user
#         except User.DoesNotExist:
#             raise exceptions.AuthenticationFailed('No such user') # raise exception if user does not exist 

#         return (user, None) # authentication successful

class CustomAuthBackend(object):
    def authenticate(self, request):
        phone = request.POST.get('username') 
        password = request.POST.get('password')

        if not phone:
            return None
        try:
            user = CustomUser.objects.get(phone=phone)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            # exception handling
            return None
        return None