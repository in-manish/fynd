from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from wars.helpers.battle_helper import get_search_queryset, BattleAggregatedData
from wars.models import Battle
from wars.serializers import BattleSerializer


class BattleListApiView(ListAPIView):
    """
        return: List of battle details
    """
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer

    def list(self, request, *args, **kwargs):
        """
            Overridden method of class:ListAPIView
            to Insert Aggregated data
        """
        queryset = self.filter_queryset(self.get_queryset())
        queryset = get_search_queryset(queryset, request.query_params)
        aggregated_data = BattleAggregatedData(queryset).get_battle_aggregated_data()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['aggregated_data'] = aggregated_data
            return response
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
