from rest_framework.generics import RetrieveAPIView

from wars.models import BattleType
from wars.serializers import BattleTypeSerializer


class BattleTypeRetrieveAPIView(RetrieveAPIView):
    queryset = BattleType.objects.all()
    serializer_class = BattleTypeSerializer
    lookup_url_kwarg = 'battle_type_id'
