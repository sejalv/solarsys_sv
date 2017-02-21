from django.core.management.base import BaseCommand, CommandError
from solarsys.models import LiveDC, LiveDCDump, ReferenceDC, InstallationKey
import sys, os, random
from datetime import datetime, date, timedelta
import numpy as np

class Command(BaseCommand):
    def handle(self, **options):
        today = datetime.now() - timedelta(days=2)
        #day_of_year = today.timetuple().tm_yday
        r1=random.random()
        ik = InstallationKey.objects.all()
        sc_max=max(ik.values('system_capacity'))
        for n in range(24): #range(24) today.hour+1
            today=today.replace(hour=n,minute=00,second=00,microsecond=00) #hour=n or today.hour
            for item in ik:
                rdc_hr = ReferenceDC.objects.get(hour=n)   #hour=n or today.hour
                live_dc_now = np.mean(rdc_hr.daily_dc) * r1 * (float(item.system_capacity)/float(sc_max['system_capacity']))
                #sc=(max(rdc_dc_today)/1000)*100/90
                LiveDCDump.objects.create(lat=item.lat, long=item.long, system_capacity=item.system_capacity, timestamp=today, dc_power=live_dc_now)
