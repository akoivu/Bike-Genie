from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.urls import reverse

class Station(models.Model):
    """A bike station"""

    name = models.CharField(max_length=100)
    # TODO: learn proper coordinate handling in Python
    address = models.CharField(max_length=70)
    city = models.CharField(max_length=20)
    capacity = models.IntegerField()
    point = models.PointField(default = Point(0,0))

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('model-detail-view', args = [str(self.id)])
