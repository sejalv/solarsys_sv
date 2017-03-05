from django.core.management.base import BaseCommand, CommandError
import sys, os, json, requests
from datetime import datetime
import secret
from solarsys.models import Reference #, Installation #, Home #InstallationKey
from solarsys import utilities

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('lat', type=int)
        parser.add_argument('lon', type=int)
        parser.add_argument('sc', type=int)

    def handle(self, **options):

        today = datetime.now()  # - timedelta(days=1)
        day_of_year = today.timetuple().tm_yday

        lat=options['lat'] #19
        lon=options['lon'] #73
        sc=options['sc']   #4 (0.05-500000)

        try:    #find existing Installation object
            ref = Reference.objects.get(lat=lat, long=lon, system_capacity=sc)

        except: #create new installation and reference DC objects, if not found
            api_key = secret.API_NREL_SECRET_KEY
            api = "https://developer.nrel.gov/api/pvwatts/v5.json?api_key=%s&lat=%d&lon=%d&system_capacity=%d&azimuth=180&tilt=%d" \
                  "&array_type=1&module_type=1&losses=10&dataset=IN&timeframe=hourly" % (api_key, lat, lon, sc, lat)

            try:  # call and load Ref API request
                req = requests.get(api)
                d = json.loads(req.content)
                if not d['errors']:
                    sys.exit(d['errors'][0])

            except:  # raise Network Exception and exit program
                sys.exit("Unexpected Network Error (API)")

            dc=utilities.createRefDC(d['outputs']['dc'])
            Reference.objects.create(lat=lat, long=lon, system_capacity=sc, dc=dc)
            print "There is/are total {} ReferenceDC objects".format(ReferenceDC.objects.count())

            # get Reference DC for the current DoY (Day of Year)
            ref = ReferenceDC.objects.get(lat=lat, long=lon, system_capacity=sc, dc__has_key=str(day_of_year - 1))

        print ref.dc[str(day_of_year - 1)]
