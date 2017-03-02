from django.conf import settings
import requests, json
from math import radians, cos, sin, asin, sqrt
import secret
from models import Reference

def create_referenceDC(lat,lon,sc):
    #create new reference objects (installation + dc), called if obj not found
    api_key = secret.API_NREL_SECRET_KEY
    api = "https://developer.nrel.gov/api/pvwatts/v5.json?api_key=%s&lat=%f&lon=%f&system_capacity=%f&azimuth=180&tilt=%f" \
          "&array_type=1&module_type=1&losses=10&dataset=IN&timeframe=hourly" % (api_key, lat, lon, sc, lat)
    print api
    try:  # call and load Ref API request
        req = requests.get(api)
        d = json.loads(req.content)
        if d['errors']:
            return str(d['errors'])
    except:  # raise Network Exception and exit program
        return "Unexpected Network Error (API)"

    d_outputs_dc = d['outputs']['dc']
    dc = {}  # 365 keys -> 24 values for each key
    for i in range(365):
        f = []
        for j in range(24):
            f.append(d_outputs_dc[i * 24 + j])
        dc[i] = f
    return dc

def genLiveDC_Hourly(refid, hr):
    ref = Reference.objects.get(id=refid)
    rdc_hr = []
    for j in range(365):
        rdc_hr.append(ref.dc[str(j)][hr])
    live_dc_now = round(random.uniform(0.1, max(rdc_hr)), 3) if max(rdc_hr) != 0 else 0
    # print str(live_dc_now) + ' / ' + str(max(rdc_hr))
    return live_dc_now


def haversine(lon1, lat1, lon2, lat2):
    # Calculates the great circle distance between two points on the earth (specified in decimal degrees)
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2]) # convert decimal degrees to radians
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r    #km

def nearest_reference(ik_long,ik_lat,ik_sc):
    ref = Reference.objects.filter(system_capacity=ik_sc)
    d = 999
    id = None
    for i in range(len(ref)):
        dist = haversine(ik_long, ik_lat, ref.values_list('long')[i][0], ref.values_list('lat')[i][0])
        if dist < d:
            d = dist
            id = ref.values_list('id')[i][0]
    return id


def sendemail(message):
    heading = "<H4>Daily Report (" + str(today.date()) + ") for low DC outputs:</H4><br><br>"
    msg = EmailMessage("Daily Report: " + str(today.date()), heading + message, settings.EMAIL_FROM, [secret.EMAIL_TO])
    msg.content_subtype = "html"
    msg.send()
