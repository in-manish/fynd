from rest_framework.serializers import ModelSerializer

from wars.models import Warrior


class WarriorSerializer(ModelSerializer):
    class Meta:
        model = Warrior
        fields = '__all__'
