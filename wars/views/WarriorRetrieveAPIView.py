from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from wars.models import Warrior
from wars.serializers import WarriorSerializer


class WarriorRetrieveAPIView(RetrieveAPIView):
    queryset = Warrior.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = WarriorSerializer
    lookup_url_kwarg = 'warrior_id'
