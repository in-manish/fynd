from rest_framework.serializers import ModelSerializer
from wars.models import Battle


class BattleSerializer(ModelSerializer):
    class Meta:
        model = Battle
        fields = '__all__'
