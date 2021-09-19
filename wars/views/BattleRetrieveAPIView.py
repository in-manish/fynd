from rest_framework.generics import RetrieveAPIView

from wars.models import Battle
from wars.serializers import BattleSerializer


class BattleRetrieveAPIView(RetrieveAPIView):
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer

    lookup_url_kwarg = 'battle_id'
