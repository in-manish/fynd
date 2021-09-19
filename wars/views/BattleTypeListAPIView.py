from rest_framework.generics import ListAPIView

from wars.models import BattleType
from wars.serializers import BattleTypeSerializer


class BattleTypeListAPIView(ListAPIView):
    queryset = BattleType.objects.order_by('title')
    serializer_class = BattleTypeSerializer
