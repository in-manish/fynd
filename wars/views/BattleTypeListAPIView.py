from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from wars.models import BattleType
from wars.serializers import BattleTypeSerializer


class BattleTypeListAPIView(ListAPIView):
    queryset = BattleType.objects.order_by('title')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = BattleTypeSerializer
