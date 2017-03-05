from django.core.management.base import BaseCommand, CommandError
import sys, os, random, math
from datetime import datetime, date, timedelta
from solarsys.models import LiveDC, Reference, InstallationKey
from solarsys import utilities

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('today', type=str)

    def handle(self, **options):
        today = datetime.strptime(options['today'], "%Y-%m-%d") if options['today'] else datetime.now() #- timedelta(days=1)
        # day_of_year = today.timetuple().tm_yday

        for ik in InstallationKey.objects.all():
            refid = utilities.nearest_reference(ik.long, ik.lat, ik.system_capacity)
            ref = Reference.objects.get(id=refid)
            for i in range(24):
                today = today.replace(hour=i, minute=00, second=00, microsecond=00)  # hour=n or today.hour
                rdc_hr = []
                for j in range(365):
                    rdc_hr.append(ref.dc[str(j)][i])
                live_dc_now = round(random.uniform(0.1, max(rdc_hr)), 3) if max(rdc_hr)!= 0 else 0
                #print str(live_dc_now) + ' / ' + str(max(rdc_hr))
                LiveDC.objects.create(installation_key=ik, timestamp=today, dc_power=live_dc_now)
