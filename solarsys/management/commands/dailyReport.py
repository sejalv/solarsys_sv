from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, date, timedelta
from solarsys import utilities

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('installation_key', type=str)
        parser.add_argument('date', type=str)

    def handle(self, **options):
        date = datetime.strptime(options['date'], "%d-%m-%Y") if options['date'] else datetime.now() #- timedelta(days=1)
        installation_key = options['installation_key'] if options['installation_key'] else "07be3461-5ffa-423c-a3c2-b02b31f1d661"

        finStr = utilities.createPerformance_daily(installation_key,date)
        if finStr:
            print finStr                    #For Dev/Test
            # utilities.sendemail(finStr)   #For PROD