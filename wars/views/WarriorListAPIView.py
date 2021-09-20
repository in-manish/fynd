from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from wars.models import Warrior
from wars.serializers import WarriorSerializer


class WarriorListAPIView(ListAPIView):
    queryset = Warrior.objects.order_by('name')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = WarriorSerializer
