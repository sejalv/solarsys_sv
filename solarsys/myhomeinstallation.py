"""
This script will send the randomly generated hourly dc power to oorjan-sv application
for given date and installation key

example usages:
python myhomeinstallation.py
python myhomeinstallation.py installation-key 2017-12-23
"""
import requests, random, sys, datetime
import settings

# randomly generate live dc
def get_live_dc():
    return round(random.uniform(1, 10000), 2)

# variable initialization
#LIVEDC_URL = "https://oorjan-sv.herokuapp.com/api/liveDC"
LIVEDC_URL = "http://localhost:8000/api/liveDC/"
MY_INSTALLATION_KEY = sys.argv[1] if len(sys.argv) > 1 else "07be3461-5ffa-423c-a3c2-b02b31f1d661"
DATE = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d") if len(sys.argv) > 2 else datetime.datetime.now()

# send hourly data
for hour in range(1,25):
    timestamp = DATE.strftime("%Y-%m-%d") + " " + str(hour)
    data = {"timestamp": timestamp, "livedc": get_live_dc(), "installation_key": MY_INSTALLATION_KEY}
    # print data
    response = requests.post(LIVEDC_URL, data=data)

#sys.exit()
