from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from wars.models import BattleType
from wars.serializers import BattleTypeSerializer


class BattleTypeRetrieveAPIView(RetrieveAPIView):
    queryset = BattleType.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = BattleTypeSerializer
    lookup_url_kwarg = 'battle_type_id'
