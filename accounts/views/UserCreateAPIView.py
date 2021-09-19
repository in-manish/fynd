from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView

from accounts.models import User
from accounts.serializers import UserSerializer
from fynd.permissions import IsSuperUser


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsSuperUser,)
    serializer_class = UserSerializer
