from django.db import models


class Warrior(models.Model):
    name = models.CharField(max_length=100)
    is_king = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'is_king': self.is_king,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
        }