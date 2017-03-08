from django.core.management.base import BaseCommand, CommandError
import sys, os, random, math
from datetime import datetime, date, timedelta
from solarsys.models import LiveDC, Reference, InstallationKey
from solarsys import utilities

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('today', type=str, nargs='?', default=datetime.now().strftime("%Y-%m-%d %H"))
        parser.add_argument('installation_key', type=str, nargs='?', default="")

    def handle(self, **options):
        today = datetime.strptime(options['today'], "%Y-%m-%d") #if options['today'] else datetime.now() #- timedelta(days=1)
        # day_of_year = today.timetuple().tm_yday
        if options['installation_key']:
            ikset = InstallationKey.objects.filter(installation_key=options['installation_key'])
        else:
            ikset = InstallationKey.objects.all()
        for ik in ikset:
            refid = utilities.nearest_reference(ik.long, ik.lat, ik.system_capacity)
            ref = Reference.objects.get(id=refid)
            len_hr = 24
            if today.date() == date.date() :
                len_hr = today.hour
            for i in range(len_hr):
                today = today.replace(hour=i, minute=00, second=00, microsecond=00)  # hour=n or today.hour
                rdc_hr = []
                for j in range(365):
                    rdc_hr.append(ref.dc[str(j)][i])
                live_dc_now = round(random.uniform(0.1, max(rdc_hr)), 3) if max(rdc_hr)!= 0 else 0
                #print str(live_dc_now) + ' / ' + str(max(rdc_hr))
                LiveDC.objects.create(installation_key=ik, timestamp=today, dc_power=live_dc_now)
