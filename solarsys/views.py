from django.shortcuts import get_object_or_404, render, HttpResponse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import Reference, LiveDC, InstallationKey
from datetime import datetime, timedelta
import utilities
import math
# Create your views here.

@csrf_exempt
def livedc_post(request, installation_key=None, date=None, errm=None):
    installation_key = get_object_or_404(InstallationKey, pk=installation_key)
    date = datetime.strptime(date, "%d-%m-%Y") if date else datetime.now()  #- timedelta(days=1)
    #form = IKForm(request.POST)
    live_dc = LiveDC()
    if request.POST:    # and form.is_valid()
        try:
            for i in range(24):
                date = date.replace(hour=i, minute=00, second=00, microsecond=00)  # date.hour
                live_dc.installation_key = installation_key
                live_dc.timestamp = date
                live_dc.dc_power = utilities.genLiveDC_Hourly(refid, i)
                #LiveDC.objects.create(installation_key=installation_key, timestamp=date, dc_power=live_dc_now)
                live_dc.save()
            # Always return an HttpResponseRedirect after successfully dealing with POST data.
            # This prevents data from being posted twice if a user hits the Back button.
            errm = "Successfully Posted"
            return HttpResponseRedirect(reverse('solarsys:api_liveDC', args=(installation_key.id,date,errm,)))
        except:
            errm = "Post failed"
            return HttpResponseRedirect(reverse('solarsys:api_liveDC', args=(installation_key.id,date,errm,)))
    errm = "From outside of request.post clause"
    context =  {'installation_key': installation_key, 'date': date, 'live_dc':live_dc, 'errm':errm}
    return render(request, 'solarsys/api_liveDC.html', context)


def performance_report(request, installation_key=None, date=None, errm=None):
    #installation_key = get_object_or_404(InstallationKey, pk=installation_key)
    date = datetime.strptime(date, "%d-%m-%Y") if date else datetime.now()  #- timedelta(days=1)

    finStr = utilities.createPerformance_daily(installation_key, date)
    all_dc = str.replace(finStr,"<br>","\n")
    #all_dc = "\n".join(finStr.split("<br>"))
    return render(request, 'solarsys/performance_report.html', {'all_dc': all_dc, 'date': date.date()
                                                                ,'installation_key':installation_key})


def reference_data(request, lat=19.07, lon=72.87, sc=10, date=None):
    date = datetime.strptime(date,"%d-%m-%Y") if date else datetime.now()
    day_of_year = date.timetuple().tm_yday
    rdc_hr_today = []
    error_message = None
    try:
        rdc = Reference.objects.get(lat__range=(math.floor(float(lat)), math.ceil(float(lat))),
                                             long__range=(math.floor(float(lon)), math.ceil(float(lon))),
                                                system_capacity=sc, dc__has_key=str(day_of_year-1))
        rdc_hr_today = rdc.dc[str(day_of_year - 1)]
    except:
        error_message = "Reference not found!"
    return render(request, 'solarsys/reference_data.html', {'rdc_hr_today':rdc_hr_today, 'date':date.date(),
                                                        'lat':lat, 'lon':lon, 'sc':sc,'error_message':error_message})


def live_data(request, installation_key=None, date=None):
    date = datetime.strptime(date, "%d-%m-%Y") if date else datetime.now()
    installation_key = InstallationKey.objects.get(installation_key=
                                            (installation_key if installation_key else "07be3461-5ffa-423c-a3c2-b02b31f1d661"))
    ldc_today = {}
    for n in range(24):  # For each hour of the day
        date = date.replace(hour=n, minute=00, second=00, microsecond=00)
        try:
            live_dc = LiveDC.objects.get(installation_key=installation_key, timestamp=date)
            ldc_today[n] = live_dc.dc_power
        except:
            break
    context = {'ldc_today':ldc_today, 'date':date.date(), 'installation_key':installation_key.installation_key}
    return render(request, 'solarsys/live_data.html', context)


def installation_key_data(request, installation_key=None):
    error_message = None
    try:
        installation_key = InstallationKey.objects.get(installation_key=(installation_key if installation_key else '86308d2b-7555-4c73-8e3f-1b963f61c1c3'))
    except:
        error_message = "InstallationKey not found!"
    return render(request, 'solarsys/installation_key_data.html', {'installation_key':installation_key, 'error_message':error_message})

