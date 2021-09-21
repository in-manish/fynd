from django.conf.urls import url

from .views import *

urlpatterns = [

    url(r'^battles$', view=BattleListApiView.as_view(), name='battle_list_api'),

    url(r'^battles/(?P<battle_id>[0-9]+)$', view=BattleRetrieveAPIView.as_view(), name='battle_retrieve_api'),

    url(r'^battle_types$', view=BattleTypeListAPIView.as_view(), name='BattleType Lists'),

    url(r'^battle_types/(?P<battle_type_id>[0-9]+)$', view=BattleTypeRetrieveAPIView.as_view(),
        name='Retrieve BattleType Detail'),

    url(r'^warriors$', view=WarriorListAPIView.as_view(), name='Warriors List'),

    url(r'^warriors/(?P<warrior_id>[0-9]+)$', view=WarriorRetrieveAPIView.as_view(), name='Retrieve Warrior Detail'),
]
