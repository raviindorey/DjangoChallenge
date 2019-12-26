from django.db import models


class Card(models.Model):
    card_name = models.CharField(max_length=25)
    card_number = models.CharField(max_length=34)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
