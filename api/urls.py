from django.conf.urls import url
from django.urls import include, path

from .views import obtain_auth_token

urlpatterns = [
    path('users/', include('users.urls')),
    url(r'api-token/', obtain_auth_token)
    #path('rest-auth/', include('rest_auth.urls')),
]
