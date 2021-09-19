from django.db import models


class Region(models.Model):
    title = models.CharField(max_length=70, db_index=True)
