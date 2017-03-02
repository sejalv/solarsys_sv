from django.core.management.base import BaseCommand, CommandError
from solarsys.models import LiveDC, Reference, InstallationKey
import sys, os, random
from datetime import datetime, date, timedelta
from solarsys import utilities
#import numpy as np

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('installation_key', type=str)
        parser.add_argument('date', type=str)

    def handle(self, **options):
        date = datetime.strptime(options['date'], "%d-%m-%Y") if options['date'] else datetime.now() #- timedelta(days=1)
        installation_key = options['installation_key'] if options['installation_key'] else "07be3461-5ffa-423c-a3c2-b02b31f1d661"
        try:
            ik = InstallationKey.objects.get(installation_key=installation_key)
            refid = utilities.nearest_reference(ik.long, ik.lat, ik.system_capacity)
            print refid
            for i in range(24):
                date = date.replace(hour=i, minute=00, second=00, microsecond=00)  # today.hour
                live_dc_now = utilities.genLiveDC_hourly(refid,i)
                #LiveDC.objects.create(installation_key=ik, timestamp=today, dc_power=live_dc_now)  #For PROD
        except:
            pass