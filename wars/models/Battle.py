from django.db import models

from .BattleType import BattleType
from .Location import Location
from .Warrier import Warrior


class Battle(models.Model):
    """
        Stores Battles detail
    """
    title = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField()
    attacker_king = models.ForeignKey(
        Warrior, related_name='attacker_king_battles', on_delete=models.CASCADE, null=True
    )
    defender_king = models.ForeignKey(
        Warrior, related_name='defender_king_battles', on_delete=models.CASCADE, null=True
    )
    attackers = models.ManyToManyField(Warrior, related_name='attackers_battles')
    defenders = models.ManyToManyField(Warrior, related_name='defenders_battles')
    battle_type = models.ForeignKey(BattleType, related_name='battle_type_battles', on_delete=models.SET_NULL,
                                    null=True)
    death = models.PositiveSmallIntegerField(default=0)
    capture = models.PositiveSmallIntegerField(default=0)
    attacker_size = models.PositiveSmallIntegerField(default=0)
    defender_size = models.PositiveSmallIntegerField(default=0)
    is_summer = models.BooleanField(default=False)
    location = models.ForeignKey(Location, related_name='location_battles', on_delete=models.SET_NULL, null=True)
    note = models.TextField(default=str, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
