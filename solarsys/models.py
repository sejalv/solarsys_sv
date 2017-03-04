from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import models
import uuid

# combined Installation and ReferenceDC tables into 1
class Reference(models.Model):
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    system_capacity = models.DecimalField(max_digits=9, decimal_places=3)
    dc = JSONField()     #key: DoY (Day of Year, starting from 0) -> values: 24 DC values (per hour) for DoY
    #added_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.id)
        #return str(self.lat) + ' - ' + str(self.long)

    class meta:
        unique_together = (('lat', 'long', 'system_capacity'))

    """
    def clean(self, *args, **kwargs):
        errors = {}
        if not isinstance(self.dc, list) or len(self.dc) != 8760:
            errors['dc'] = 'DC must be an array containing 8760 data points.'
        if bool(errors):
            raise ValidationError(errors)
        super(Reference, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Reference, self).save(*args, **kwargs)
    """


# added new model for InstallationKey
class InstallationKey(models.Model):
    installation_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    system_capacity = models.DecimalField(max_digits=7, decimal_places=4)
    #installation_id = models.ForeignKey(Reference)
    #added_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.installation_key)


# initially called LiveDCDump
class LiveDC(models.Model):
    installation_key = models.ForeignKey(InstallationKey)
    timestamp = models.DateTimeField()
    dc_power = models.DecimalField(max_digits=9, decimal_places=4)
    #    added_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.installation_key)




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
