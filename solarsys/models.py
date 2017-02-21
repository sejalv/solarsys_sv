from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.

#Not Required, but has all JSON data
class SolarReference(models.Model):
    name = models.CharField(max_length=200)
    data = JSONField()

    def __unicode__(self):
        return self.name

class InstallationKey(models.Model):
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    system_capacity = models.DecimalField(max_digits=7, decimal_places=4)

    def __unicode__(self):
        return self.id

class ReferenceDC(models.Model):
    installation_key = models.ForeignKey(InstallationKey)
    hour = models.IntegerField()
    daily_dc = JSONField()

    def __unicode__(self):
        return self.hour

# For future: Live data will be moved here after daily report is created
class LiveDC(models.Model):
    installation_key = models.ForeignKey(InstallationKey)
    hour = models.IntegerField()
    daily_dc = JSONField()

    def __unicode__(self):
        return self.hour

# Live data will be inserted here during simulation
class LiveDCDump(models.Model):
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    system_capacity = models.DecimalField(max_digits=7, decimal_places=4)
    timestamp = models.DateTimeField()
    dc_power = models.DecimalField(max_digits=10, decimal_places=5)

    def __unicode__(self):
        return self.dc_power