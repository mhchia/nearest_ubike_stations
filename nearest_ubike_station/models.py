from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Station(models.Model):

    name = models.CharField(max_length=100)
    num_bikes = models.IntegerField()
    lat = models.FloatField()
    lng = models.FloatField()

    def __unicode__(self):

        return self.name
