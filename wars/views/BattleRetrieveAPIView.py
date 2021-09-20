from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from wars.models import Battle
from wars.serializers import BattleSerializer


class BattleRetrieveAPIView(RetrieveAPIView):
    queryset = Battle.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = BattleSerializer

    lookup_url_kwarg = 'battle_id'
