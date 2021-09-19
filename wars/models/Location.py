from django.db import models

from .Region import Region


class Location(models.Model):
    title = models.CharField(max_length=80, db_index=True, null=True)
    region = models.ForeignKey(Region, related_name='region_locations', on_delete=models.CASCADE)
