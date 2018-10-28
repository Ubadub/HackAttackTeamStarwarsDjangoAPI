from django.urls import include, path

from .views import *

urlpatterns = [
    path('', UserListView.as_view()),
    path('emergency-contacts/', EmergencyContactsListView.as_view()),
    path('login/', LoginView.as_view()),
    path('api-token/', TokenView.as_view()),
    #path('self/', views.UserListView.as_view()), # TODO
]