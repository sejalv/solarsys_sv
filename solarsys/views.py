from django.shortcuts import get_object_or_404, render, HttpResponse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import Reference, LiveDC, InstallationKey
from datetime import datetime, timedelta
import requests
import utilities
# Create your views here.

@csrf_exempt
def livedc_post(request, ik=None, today=None, errm=None):
    ik = get_object_or_404(InstallationKey, pk=ik)
    today = datetime.strptime(today, "%d-%m-%Y") if today else datetime.now()  #- timedelta(days=1)
    #form = IKForm(request.POST)
    live_dc = LiveDC()
    if request.POST:    # and form.is_valid()
        try:
            for i in range(24):
                today = today.replace(hour=i, minute=00, second=00, microsecond=00)  # today.hour
                live_dc.installation_key = ik
                live_dc.timestamp = today
                live_dc.dc_power = utilities.genLiveDC_Hourly(refid, i)
                #LiveDC.objects.create(installation_key=ik, timestamp=today, dc_power=live_dc_now)
                live_dc.save()
            # Always return an HttpResponseRedirect after successfully dealing with POST data.
            # This prevents data from being posted twice if a user hits the Back button.
            errm = "Successfully Posted"
            return HttpResponseRedirect(reverse('solarsys:api_liveDC', args=(ik.id,today,errm,)))
        except:
            errm = "Post failed"
            return HttpResponseRedirect(reverse('solarsys:api_liveDC', args=(ik.id,today,errm,)))
    errm = "From outside of request.post clause"
    return render(request, 'solarsys/api_liveDC.html', {'ik': ik, 'today': today, 'live_dc':live_dc, 'errm':errm})


def performance_report(request, today=None):
    if not today:
        today = datetime.today() - timedelta(days=1)
    day_of_year = today.timetuple().tm_yday
    it = InstallationKey.objects.all()
    all_dc = {}
    for n in range(today.hour + 1):  # For each hour of the day
        today = today.replace(hour=n, minute=00, second=00, microsecond=00)
        for i in it:  # For each Installation
            try:
                rdc_hr = Reference.objects.get(hour=n, installation_id=i.id)
                rdc_hr_today = rdc_hr.daily_dc[day_of_year - 1]
            except:
                continue
            ldc_hr_today = LiveDC.objects.filter(lat=i.lat, long=i.long, system_capacity=i.system_capacity,
                                                 timestamp=today).values('dc_power').first()
            try:
                if ldc_hr_today['dc_power'] < (rdc_hr_today * 80 / 100):
                    all_dc[n] = [ldc_hr_today['dc_power'], rdc_hr_today, rdc_hr_today * 80 / 100, i.id]
            except:
                continue

    context = {'all_dc': all_dc, 'today': today.date()}
    return render(request, 'solarsys/performance_report.html', context)


def reference_data(request, lat=19.07, lon=72.87, sc=4, today=datetime.today()):
    day_of_year = today.timetuple().tm_yday
    rdc_hr_today = None
    error_message = None
    try:
        rdc_hr_today = Reference.objects.get(lat=lat, long=lon, system_capacity=sc, dc__has_key=str(day_of_year-1))
    except:
        error_message = "Reference not found!"
    return render(request, 'solarsys/reference_data.html', {'rdc_hr_today':rdc_hr_today.dc[str(day_of_year - 1)], 'today':today.date(),
                                                        'lat':lat, 'lon':lon, 'sc':sc,'error_message':error_message})


def live_data(request, ik=None, today=datetime.today()):
    ik = InstallationKey.objects.get(installation_key=(ik if ik else "07be3461-5ffa-423c-a3c2-b02b31f1d661"))
    ldc_today = {}
    for n in range(today.hour+1):  # For each hour of the day
        today = today.replace(hour=n, minute=00, second=00, microsecond=00)
        ldc_hr_today = LiveDC.objects.filter(lat=ik.lat, long=ik.long, system_capacity=ik.system_capacity,
                                             timestamp=today).values('dc_power').first()
        ldc_today[n] = ldc_hr_today['dc_power']

    return render(request, 'solarsys/live_data.html', {'ldc_today':ldc_today, 'today':today.date(), 'ik':ik.id})


def installation_key_data(request, ik=None):
    error_message = None
    try:
        ik = InstallationKey.objects.get(installation_key=(ik if ik else '86308d2b-7555-4c73-8e3f-1b963f61c1c3'))
    except:
        error_message = "InstallationKey not found!"
    return render(request, 'solarsys/installation_key_data.html', {'ik':ik, 'error_message':error_message})

