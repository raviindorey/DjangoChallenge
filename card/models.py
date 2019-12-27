from django.db import models
from .utils import create_hyphen_string


class Card(models.Model):
    card_name = models.CharField(max_length=25)
    card_number = models.CharField(max_length=34)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.card_name} {create_hyphen_string(self.card_number)}"
