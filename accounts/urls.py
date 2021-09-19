from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^obtain_token$', view=views.ObtainTokenAPIView.as_view(), name='Obtain Auth Token'),

    url(r'^user$', view=views.UserCreateAPIView.as_view(), name='Create User'),
]
