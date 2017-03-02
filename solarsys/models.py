from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import models
import uuid

# altered columns - daily_dc to dc
class Reference(models.Model):
    #installation_id = models.ForeignKey(Installation)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    system_capacity = models.DecimalField(max_digits=9, decimal_places=3)
    dc = JSONField()     #key: DoY (Day of Year, starting from 0) -> values: 24 DC values (per hour) for DoY

    """
    def __unicode__(self):
        return self.id

    def getDCToday(self, doy):
        return self.dc[doy]
    """

# added new model for InstallationKey
class InstallationKey(models.Model):
    installation_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    system_capacity = models.DecimalField(max_digits=7, decimal_places=4)

    """
    def __unicode__(self):
        return self.installation_key
    """

# initially called LiveDCDump
class LiveDC(models.Model):
    installation_key = models.ForeignKey(InstallationKey)
    timestamp = models.DateTimeField()
    dc_power = models.DecimalField(max_digits=9, decimal_places=4)

    def __unicode__(self):
        return self.dc_power


"""
#Not used/referenced in code, but may have all JSON data for each reference API call
class SolarReference(models.Model):
    name = models.CharField(max_length=200)
    data = JSONField()

    def __unicode__(self):
        return self.name


#Not used/referenced in code, initially called InstallationKey
class Installation(models.Model):
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    system_capacity = models.DecimalField(max_digits=7, decimal_places=4)

    def __unicode__(self):
        return self.id
"""
"""
# For future: Live data dump may be moved here after daily report is created
class LiveDC(models.Model):
    installation_id = models.ForeignKey(Installation)
    date = models.DateTimeField()
    dc_hourly = JSONField()

    def __unicode__(self):
        return self.hour
"""