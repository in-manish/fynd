from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from wars.helpers.battle_helper import get_search_queryset, BattleAggregatedData
from wars.models import Battle
from wars.serializers import BattleSerializer


class BattleListApiView(ListAPIView):
    """
        return: List of battle details
    """
    queryset = Battle.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = BattleSerializer

    def get_sorted_queryset(self, queryset):
        """
            ---Sort Queryset----
            sort_fields: fields on sorting can apply

            eg. ?sort_for=title;sort_order=desc
        """
        sort_fields = ['title', 'year', 'battle_number',
                       'attacker_king', 'defender_king',
                       'battle_type', 'created_at', 'modified_at']
        query_params = self.request.query_params
        sort_for = query_params.get('sort_for')
        sort_order = query_params.get('sort_order')
        if not sort_for or sort_for not in sort_fields:
            sort_for = 'created_at'
        if sort_order:
            if sort_order == 'desc':
                sort_for = f"-{sort_for}"

        queryset = queryset.order_by(sort_for)
        return queryset

    def list(self, request, *args, **kwargs):
        """
            Overridden method of class:ListAPIView
            to Insert search queryset, sort queryset and Aggregated data
        """
        queryset = self.filter_queryset(self.get_queryset())
        queryset = get_search_queryset(queryset, request.query_params)
        queryset = self.get_sorted_queryset(queryset)
        aggregated_data = BattleAggregatedData(queryset).get_battle_aggregated_data()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['aggregated_data'] = aggregated_data
            return response
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
