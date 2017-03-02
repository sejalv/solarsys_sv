from django.conf import settings
import requests, json, random
from math import radians, cos, sin, asin, sqrt
import secret
from .models import LiveDC, Reference, InstallationKey

def create_referenceDC(lat,lon,sc): #create new reference objects (installation + dc), called if obj not found
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

def genLiveDC_hourly(refid, hr):
    ref = Reference.objects.get(id=refid)
    rdc_hr = []
    for j in range(365):
        rdc_hr.append(ref.dc[str(j)][hr])
    live_dc_now = round(random.uniform(0.1, max(rdc_hr)), 3) if max(rdc_hr) != 0 else 0
    print str(hr) +': '+ str(live_dc_now) + ' / ' + str(max(rdc_hr))
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

def createPerformance_daily(installation_key,date):
    try:
        ik = InstallationKey.objects.get(installation_key=installation_key)
        refid = nearest_reference(ik.long, ik.lat, ik.system_capacity)
        day_of_year = date.timetuple().tm_yday
        finStr=""
        for i in range(24):
            try:
                rdc = Reference.objects.get(id=refid)
                rdc_hr = rdc.dc[str(day_of_year-1)][i]
                date = date.replace(hour=i, minute=00, second=00, microsecond=00)
                ldc = LiveDC.objects.get(installation_key=installation_key, timestamp=date)
                if ldc.dc_power < rdc_hr * 80/100:
                    str1 = "Hour: %d:00:00 <br> Live Data: %f < 80%% of Ref Data: %f <br><br>" %(i, ldc.dc_power, rdc_hr)
                    finStr = finStr + str1
            except:
                break
        return finStr
    except:
        return None

def sendemail(message):
    heading = "<H4>Daily Report (" + str(today.date()) + ") for low DC outputs:</H4><br><br>"
    msg = EmailMessage("Daily Report: " + str(today.date()), heading + message, settings.EMAIL_FROM, [secret.EMAIL_TO])
    msg.content_subtype = "html"
    msg.send()
