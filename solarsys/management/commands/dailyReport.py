from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, date, timedelta
from solarsys import utilities
from solarsys.models import InstallationKey

class Command(BaseCommand):
    def add_arguments(self, parser):
        #parser.add_argument('installation_key', type=str)
        parser.add_argument('date', type=str, nargs='?', default=datetime.now().strftime("%d-%m-%Y"))

    def handle(self, **options):

        date = datetime.strptime(options['date'], "%d-%m-%Y") #if options['date'] else datetime.now() #- timedelta(days=1)
        #installation_key = options['installation_key'] if options['installation_key'] else "07be3461-5ffa-423c-a3c2-b02b31f1d661"

        for i in InstallationKey.objects.all():
            msg = utilities.dailyPerformance(i.installation_key,date)
            message = msg if msg else "No data for this day or installation key: "+str(i.installation_key)+"!"
            heading = "<H4>Daily Report (" + str(date.date()) + ") with low DC Power values for " \
                        "Installation Key: {installationkey} <br>  </H4><br><br>".format(installationkey=str(i.installation_key))

            print heading + message
            # Uncomment For PROD/Test
            utilities.sendemail(heading+message)
