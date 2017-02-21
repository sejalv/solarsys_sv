import sys, os
import json
#import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oorjan_sv.settings")

import django
django.setup()

from solarsys.models import SolarReference, ReferenceDC, InstallationKey
    
if __name__ == "__main__":
    
    if len(sys.argv) >= 2:
        print "Reading from file " + str(sys.argv[1])

        with open(sys.argv[1]) as json_data:
            d= json.load(json_data)

        if len(sys.argv) == 2:
            for item in d:
                SolarReference.objects.create(name=item, data=d[item])
            print "There are {} SolarReference objects".format(SolarReference.objects.count())

            InstallationKey.objects.create(lat=d['inputs']['lat'], long=d['inputs']['lon'],
                                           system_capacity=d['inputs']['system_capacity'])
            print "There is/are {} InstallationKey objects".format(InstallationKey.objects.count())

        elif sys.argv[2]=="dc":

            items=d['outputs']['dc']
            ik = InstallationKey.objects.get(lat=d['inputs']['lat'], long=d['inputs']['lon'],
                                             system_capacity=d['inputs']['system_capacity'])
            '''
            # 365 rows x 24 cols
            for i in range(24):
                f = []
                for j in range(365):
                    f.append(items[i*365+j])
                #ReferenceDC.objects.create(hour=i, dc_power=f)
                print str(i) +'->'+ str(len(f)) +'->'+ str(f)
            '''
            # 24 rows x 365 cols
            for i in range(24):
                f = []
                for j in range(365):
                    f.append(items[j*24+i])
                ReferenceDC.objects.create(installation_key=ik, hour=i, daily_dc=f)
                print str(i) +'->'+ str(len(f)) #+'->'+ str(f)
                print '\n'
            print "There are {} ReferenceDC objects".format(ReferenceDC.objects.count())

    else:
        print "Please, provide Reference file path"
