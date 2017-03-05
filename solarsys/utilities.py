from django.conf import settings
from django.core.mail import EmailMessage
import requests, json, random
from math import radians, cos, sin, asin, sqrt
from datetime import datetime, date, timedelta
from haversine import haversine
import secret1
from .models import LiveDC, Reference, InstallationKey

def getRefDC_API(lat,lon,sc): # fetches and returns 365 x 24 DC Power values for each installation (ref obj)
    api_key = secret1.API_NREL_SECRET_KEY
    #api = "https://developer.nrel.gov/api/pvwatts/v5.json?api_key=%s&lat=%f&lon=%f&system_capacity=%f&azimuth=180&tilt=%f" \
    #      "&array_type=1&module_type=1&losses=10&dataset=IN&timeframe=hourly" % (api_key, lat, lon, sc, lat)
    api ='https://developer.nrel.gov/api/pvwatts/v5.json?api_key={api_key}&lat={lat}&lon={long}' \
         '&system_capacity={system_capacity}&azimuth=180&tilt={lat}&array_type=1&module_type=1&losses=10' \
         '&dataset=IN&timeframe=hourly'.format(api_key=api_key,lat=lat, long=lon, system_capacity=sc)
    print api
    try:   # call and load Ref API request
        req = requests.get(api)
        d = json.loads(req.content)
        if d['errors']:
            return str(d['errors'])
    except:
        return "Unexpected Network Error (API)"

    d_outputs_dc = d['outputs']['dc']
    dc = {}
    for i in range(365):
        f = []
        for j in range(24):
            f.append(d_outputs_dc[i * 24 + j])
        dc[i] = f
    return dc   # 365 keys -> 24 values for each key


def nearest_reference(ik_lat,ik_long,ik_sc):    # finds and returns nearest reference obj id for an installation key
    nearby_station = [None, 999999999999]
    ref = Reference.objects.filter(system_capacity=ik_sc)
    if len(ref):
        for i in range(len(ref)):
            source_point = (ik_lat, ik_long)
            destination_point = (ref.values_list('lat')[i][0], ref.values_list('long')[i][0])
            distance = haversine(source_point, destination_point)
            if distance < nearby_station[1]:
                nearby_station[0] = ref.values_list('id')[i][0]
                nearby_station[1] = distance
    return nearby_station[0]       # refid or None


def genLiveDC_hourly(ik, hr):    # generates and returns DC power by the hour for an installation key
    try:
        ik = InstallationKey.objects.get(installation_key=ik)
        refid = nearest_reference(ik.lat,ik.long,ik.system_capacity)
        ref = Reference.objects.get(id=refid)

        rdc_hr = []
        for j in range(365):
            rdc_hr.append(ref.dc[str(j)][hr])
        live_dc_now = round(random.uniform(0.1, max(rdc_hr)), 3) if max(rdc_hr) != 0 else 0
        #print str(hr) +': '+ str(live_dc_now) + ' / ' + str(max(rdc_hr))    # comment in PROD
        return live_dc_now
    except:
        return 0.0


def dailyPerformance(installation_key,date):    # measures performance of Live DC wrt. Ref DC for each hour of the day
    try:
        ik = InstallationKey.objects.get(installation_key=installation_key)
        refid = nearest_reference(ik.lat, ik.long, ik.system_capacity)
        ref = Reference.objects.get(id=refid)
        livedcs = LiveDC.objects.filter(installation_key=ik, timestamp__date=date.date()).order_by('timestamp')
        day_of_year = date.timetuple().tm_yday
        msg=""
        for ldc in livedcs:
            rdc = ref.dc[str(day_of_year-1)][ldc.timestamp.hour]
            #if ldc.values('dc_power')[0] < rdc_hr * 80/100:
            if ldc.dc_power < rdc * 0.8:     # comparing live DC with 80% of ref DC
                msg += 'Timestamp: {timestamp} <br> ' \
                       'Live DC Power: {live_dc_power}  < 80%% of Reference DC Power: {reference_dc_power}<br>' \
                       '<br>'.format(timestamp=ldc.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                                     , live_dc_power=ldc.dc_power, reference_dc_power=rdc)

        return msg
    except:
        return None

def sendemail(message):     # function that creates and sends email for Daily Report
    msg = EmailMessage("Daily Report - Lower LiveDC values", message, settings.EMAIL_FROM, secret1.EMAIL_TO)
    msg.content_subtype = "html"
    msg.send()


"""
### OBSOLETE ###
#using haversine lib now
def haversine(lon1, lat1, lon2, lat2): # Calculates great circle distance between two points on earth (specified in decimal degrees)
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2]) # convert decimal degrees to radians
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r    #km
"""
