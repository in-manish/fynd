from typing import Dict

from django.db.models import Q, Count, F, Avg, Min, Max

__all__ = (
    'BattleAggregatedData',
    'get_search_queryset',
)


class BattleAggregatedData:
    def __init__(self, queryset):
        self.queryset = queryset

    def get_battle_aggregated_data(self) -> Dict:
        """
            all combined aggregated data
        """
        data = {
            **self.get_battle_type_battles_aggr_data(),
            **self.get_attacker_max_battle_aggr_data(),
            **self.get_defender_max_battle_aggr_data(),
            **self.get_min_max_avg_defender_aggr_data()
        }
        return data

    def get_battle_type_battles_aggr_data(self):
        """
            Count of Battles per battle type
        """
        values = (self.queryset
                  .values('battle_type_id')
                  .annotate(battle_count=Count('battle_type_id'),
                            id=F('battle_type_id'),
                            title=F('battle_type__title'))
                  .values('id', 'title', 'battle_count'))
        data = {'battle_types': values}
        return data

    def get_min_max_avg_defender_aggr_data(self):
        """
            Min, Max, Avg of defender size
        """
        aggregated_data = (self.queryset
                           .aggregate(min_defender_size=Min('defender_size'),
                                      max_defender_size=Max('defender_size'),
                                      avg_defender_size=Avg('defender_size'))
                           )
        data = {'defender_statistics': aggregated_data}
        return data

    def get_attacker_max_battle_aggr_data(self):
        """
            Most active Attacker King data
        """
        data: dict = (self.queryset
                      .values('attacker_king_id', name=F('attacker_king__name'))
                      .annotate(battle_count=Count('attacker_king_id'))
                      .order_by('-battle_count').first())
        data['id'] = data.pop('attacker_king_id')
        data = {
            'max_battle_attacker': data
        }
        return data

    def get_defender_max_battle_aggr_data(self):
        """
            Most active Defender King data
        """
        data: dict = (self.queryset
                      .values('defender_king_id', name=F('defender_king__name'))
                      .annotate(battle_count=Count('defender_king_id'))
                      .order_by('-battle_count').first())
        data['id'] = data.pop('defender_king_id')
        data = {
            'max_battle_defender': data
        }
        return data


def get_search_queryset(queryset, query_params):
    """
        Search word on Battle related attribute
        searching fields: battle, year, location, region, attacker_king, defender_king, battle_king
        query_params:-
            -search_key: field on which search will apply
            -search_word: searching word
    """
    search_key = query_params.get('search_key')
    search_word = query_params.get('search_word')
    if not search_key or not search_word:
        return queryset
    search_key = search_key.strip()
    search_word = search_word.strip()
    search_query_data = {
        'battle': Q(title__icontains=search_word),
        'year': Q(year=search_word),
        'location': Q(location__title__icontains=search_word),
        'region': Q(location__region__title__icontains=search_word),
        'attacker_king': Q(attacker_king__name__icontains=search_word),
        'defender_king': Q(defender_king__name__icontains=search_word),
        'battle_type': Q(battle_type__title__icontains=search_word),
    }
    search_query = search_query_data.get(search_key)
    if search_query:
        queryset = queryset.filter(search_query)
    return queryset
