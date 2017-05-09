from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Station(models.Model):

    station = models.CharField(max_length=100)
    num_ubike = models.IntegerField()
    lat = models.FloatField()
    lng = models.FloatField()

    def __unicode__(self):

        return self.name
