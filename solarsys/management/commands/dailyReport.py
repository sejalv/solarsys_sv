from django.core.management.base import BaseCommand, CommandError
from solarsys.models import LiveDC, LiveDCDump, ReferenceDC, InstallationKey
import sys, os, random
from datetime import datetime, date, timedelta
import numpy as np
from django.core.mail import EmailMessage
from django.conf import settings

class Command(BaseCommand):

    '''
    def add_arguments(self, parser):
        parser.add_argument('today', type=datetime)
    '''

    def handle(self, **options):

        '''
        if options['today']:
            today = options['today']
        else:
        '''

        today = datetime.now() #- timedelta(days=1)
        day_of_year = today.timetuple().tm_yday
        ik = InstallationKey.objects.all()
        finStr=""
        for n in range(today.hour+1): # For each hour of the day #range(today.hour+1) or 24
            today = today.replace(hour=n, minute=00, second=00, microsecond=00)
            for i in ik:  # For each InstallationKey
                try:
                    rdc_hr = ReferenceDC.objects.get(hour=n, installation_key=i.id)
                    rdc_hr_today = rdc_hr.daily_dc[day_of_year-1]
                except:
                    continue
                ldc_hr_today = LiveDCDump.objects.filter(lat=i.lat, long=i.long, system_capacity=i.system_capacity,timestamp=today).values('dc_power').first()
                if ldc_hr_today['dc_power'] < (rdc_hr_today * 80/100) :
                    str1= 'Hour: %d:00:00 <br> Live Data: %f < 80%% of Ref Data: %f <br><br>' %(n, ldc_hr_today['dc_power'], rdc_hr_today)
                    finStr=finStr+str1
        #print finStr

        def sendemail(message):
            heading="<H4>Daily Report ("+str(today.date())+") for low DC outputs:</H4><br><br>"
            msg = EmailMessage("Daily Report: "+str(today.date()), heading+message, settings.EMAIL_FROM, ['sejal.v18@gmail.com'])
            msg.content_subtype = "html"
            msg.send()

        sendemail(finStr)