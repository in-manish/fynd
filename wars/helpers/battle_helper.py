from typing import Dict

from django.core.cache import cache
from django.db import connection
from django.db.models import Q

__all__ = (
    'BattleAggregatedData',
    'get_search_queryset',
)


class BattleAggregatedData:
    def __init__(self, queryset):
        self.battle_ids = list(queryset.values_list('id', flat=True))
        self.tuple_battle_ids = tuple(self.battle_ids)

    def get_battle_aggregated_data(self) -> Dict:
        """
            all combined aggregated data
        """
        cache_key = 'battle_aggr_data_key'
        data = cache.get(cache_key)
        if data:
            return data
        with connection.cursor() as cursor:
            data = {
                **self.get_battle_type_battles_aggr_data(cursor),
                **self.get_attacker_max_battle_aggr_data(cursor),
                **self.get_defender_max_battle_aggr_data(cursor),
                **self.get_min_max_avg_defender_aggr_data(cursor)
            }
        expire_in = 60 * 60 * 24  # 1day
        cache.set(cache_key, data, expire_in)
        return data

    def get_battle_type_battles_aggr_data(self, cursor):
        """
            Count of Battles per battle type
        """
        data = {'battle_types': []}
        if not self.tuple_battle_ids:
            return data
        sql_query = f"""
            SELECT battle_type.id, battle_type.title, COUNT(battle_type.id) FROM wars_battle AS battle
            
            INNER JOIN wars_battletype AS battle_type
            ON battle_type.id=battle.battle_type_id
            
            WHERE battle.id IN {self.tuple_battle_ids}
            
            GROUP BY battle_type.id, battle_type.title
        """
        cursor.execute(sql_query)
        results = cursor.fetchall()

        for result in results:
            obj = {
                'id': result[0],
                'title': result[1],
                'battle_count': result[2]
            }
            data['battle_types'].append(obj)
        return data

    def get_min_max_avg_defender_aggr_data(self, cursor):
        """
            Min, Max, Avg of defender size
        """
        data = {
            'defender_statistics': {
                'min_defender_size': 0,
                'max_defender_size': 0,
                'avg_defender_size': 0,
            }
        }
        if not self.tuple_battle_ids:
            return data
        sql_query = f"""
                SELECT MIN(defender_size), MAX(defender_size), AVG(defender_size) FROM wars_battle
                WHERE id IN {self.tuple_battle_ids}
            """
        cursor.execute(sql_query)
        result = cursor.fetchone()
        data = {
            'defender_statistics': {
                'min_defender_size': result[0],
                'max_defender_size': result[1],
                'avg_defender_size': result[2],
            }
        }
        return data

    def get_attacker_max_battle_aggr_data(self, cursor):
        """
            Most active Attacker King data
        """
        data = {'max_battle_attacker': {}}
        if not self.tuple_battle_ids:
            return data
        sql_query = f"""
                SELECT attacker_king_id, warrior.name, COUNT(attacker_king_id) FROM wars_battle AS battle
                
                INNER JOIN wars_warrior AS warrior
                ON  battle.attacker_king_id=warrior.id
                
                WHERE battle.id IN {self.tuple_battle_ids}
    
                GROUP BY attacker_king_id, warrior.name
    
                ORDER BY COUNT(attacker_king_id) DESC LIMIT 1;
            """
        cursor.execute(sql_query)
        result = cursor.fetchone()
        data = {
            'max_battle_attacker': {
                'id': result[0],
                'name': result[1],
                'battle_count': result[2]
            }
        }
        return data

    def get_defender_max_battle_aggr_data(self, cursor):
        """
            Most active Defender King data
        """
        data = {'max_battle_defender': {}}
        if not self.tuple_battle_ids:
            return data
        sql_query = f"""
                SELECT defender_king_id, warrior.name, COUNT(defender_king_id) FROM wars_battle AS battle
                
                INNER JOIN wars_warrior AS warrior
                ON  battle.defender_king_id=warrior.id
                
                WHERE battle.id IN {self.tuple_battle_ids}

                GROUP BY defender_king_id, warrior.name

                ORDER BY COUNT(defender_king_id) DESC LIMIT 1;
            """
        cursor.execute(sql_query)
        cursor.execute(sql_query)
        result = cursor.fetchone()
        data = {
            'max_battle_defender': {
                'id': result[0],
                'name': result[1],
                'battle_count': result[2]
            }
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
