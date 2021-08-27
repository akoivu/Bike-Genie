from django.db import models
from django.urls import reverse

class Station(models.Model):
    """A bike station"""

    name = models.CharField(max_length=100)
    # TODO: learn proper coordinate handling in Python
    x = models.CharField(max_length=50)
    y = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('model-detail-view', args = [str(self.id)])