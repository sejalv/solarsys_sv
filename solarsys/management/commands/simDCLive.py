from django.core.management.base import BaseCommand, CommandError
from solarsys.models import LiveDC, Reference, InstallationKey
import sys, os, random
from datetime import datetime, date, timedelta
import utilities
#import numpy as np

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('today', type=str)
        parser.add_argument('ikey', type=str)

    def handle(self, **options):
        today = datetime.strptime(options['today'], "%Y-%m-%d") if options['today'] else datetime.now() #- timedelta(days=1)
        # day_of_year = today.timetuple().tm_yday
        ikey = options['ikey'] if options['ikey'] else "07be3461-5ffa-423c-a3c2-b02b31f1d661"

        ik = InstallationKey.objects.get(installation_key=ikey)
        refid = utilities.nearest_reference(ik.long, ik.lat, ik.system_capacity)

        for i in range(24):
            today = today.replace(hour=i, minute=00, second=00, microsecond=00)  # today.hour
            live_dc_now = utilities.genLiveDC_Hourly(refid,i)
            LiveDC.objects.create(installation_key=ik, timestamp=today, dc_power=live_dc_now)
