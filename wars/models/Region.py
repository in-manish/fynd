from django.db import models


class Region(models.Model):
    title = models.CharField(unique=True, max_length=70, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
