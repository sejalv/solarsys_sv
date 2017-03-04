"""
This script will send the randomly generated hourly dc power to oorjan-sv application for given date and installation key
example usages:
python manage.py simulatelivddc
python manage.py simulatelivedc <installation_key> <2017-12-23>
"""
from django.core.management.base import BaseCommand, CommandError
import requests, random, sys
from datetime import datetime
from solarsys import utilities

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('MY_INSTALLATION_KEY', type=str)
        parser.add_argument('DATE', type=str, nargs='?', default=datetime.now().strftime("%Y-%m-%d"))

    def handle(self, **options):
        LIVEDC_URL = "https://oorjan-sv.herokuapp.com/solarsys/api/livedc"
        #LIVEDC_URL = "http://localhost:8000/solarsys/api/livedc/"
        MY_INSTALLATION_KEY = options['MY_INSTALLATION_KEY'] #if options['MY_INSTALLATION_KEY'] else "07be3461-5ffa-423c-a3c2-b02b31f1d661"
        DATE = datetime.strptime(options['DATE'], "%Y-%m-%d") #if options['DATE'] else datetime.now() #- timedelta(days=1)

        # simulate hourly data
        for hour in range(0,24):
            timestamp = DATE.strftime("%Y-%m-%d") + " " + str(hour)
            data = {"timestamp":timestamp, "dcpower":utilities.genLiveDC_hourly(MY_INSTALLATION_KEY,hour), "installationkey":MY_INSTALLATION_KEY}
            print data
            response = requests.post(LIVEDC_URL, data=data)
            print response.text if response.status_code in [201, 400] else "Error: " + str(response.status_code) + "\n"
        print LIVEDC_URL+