from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^battles', view=BattleListApiView.as_view(), name='battle_list_api'),

    url(r'^battles/(?P<battle_id>[0-9]+)$', view=BattleRetrieveAPIView.as_view(), name='battle_retrieve_api'),

    url(r'^battle_types$', view=BattleTypeListAPIView.as_view(), name='BattleType Lists'),

    url(r'^battle_types/(?P<battle_type_id>[0-9]+)$', view=BattleTypeRetrieveAPIView.as_view(),
        name='Retrieve BattleType Detail'),
]
