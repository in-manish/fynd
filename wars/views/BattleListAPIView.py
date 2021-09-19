from rest_framework.generics import ListAPIView

from wars.models import Battle
from wars.serializers import BattleSerializer


class BattleListApiView(ListAPIView):
    """
        return: List of battle details
    """
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer
