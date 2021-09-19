from rest_framework.serializers import ModelSerializer

from wars.models import BattleType


class BattleTypeSerializer(ModelSerializer):
    class Meta:
        model = BattleType
        fields = '__all__'
