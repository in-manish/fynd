from django.db import models


class BattleType(models.Model):
    title = models.CharField(max_length=50, db_index=True)
