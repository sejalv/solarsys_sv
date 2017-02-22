from django.shortcuts import get_object_or_404, render, HttpResponse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from .models import ReferenceDC, LiveDCDump, InstallationKey
from datetime import datetime
# Create your views here.

def reference_data(request, ik=None, today=None):
    if not today:
        today = datetime.today() #- timedelta(days=1)
    day_of_year = today.timetuple().tm_yday
    if not ik:
        ik = InstallationKey.objects.get(id=1)
    rdc_hr_today={}
    for n in range(24):  # For each hour of the day
        today = today.replace(hour=n, minute=00, second=00, microsecond=00)
        try:
            rdc_hr = ReferenceDC.objects.get(hour=n, installation_key=ik.id)
            rdc_hr_today[n] = rdc_hr.daily_dc[day_of_year - 1]
        except:
            continue
    return render(request, 'solarsys/reference_data.html', {'rdc_hr_today':rdc_hr_today, 'today':today.date(), 'ik':ik.id})


def live_data(request, ik=None, today=None):
    if not today:
        today = datetime.today() #- timedelta(days=1)
    #day_of_year = today.timetuple().tm_yday
    if not ik:
        ik = InstallationKey.objects.get(id=1)
    ldc_today = {}
    for n in range(today.hour+1):  # For each hour of the day
        today = today.replace(hour=n, minute=00, second=00, microsecond=00)
        ldc_hr_today = LiveDCDump.objects.filter(lat=ik.lat, long=ik.long, system_capacity=ik.system_capacity,
                                             timestamp=today).values('dc_power').first()
        ldc_today[n] = ldc_hr_today['dc_power']

    return render(request, 'solarsys/live_data.html', {'ldc_today':ldc_today, 'today':today.date(), 'ik':ik.id})


def performance_report(request, today=None):
        if not today:
            today = datetime.today()  # - timedelta(days=1)
        day_of_year = today.timetuple().tm_yday
        ik = InstallationKey.objects.all()
        all_dc = {}
        for n in range(today.hour+1):  # For each hour of the day
            today = today.replace(hour=n, minute=00, second=00, microsecond=00)
            for i in ik:  # For each InstallationKey
                try:
                    rdc_hr = ReferenceDC.objects.get(hour=n, installation_key=i.id)
                    rdc_hr_today = rdc_hr.daily_dc[day_of_year - 1]
                except:
                    continue
                ldc_hr_today = LiveDCDump.objects.filter(lat=i.lat, long=i.long, system_capacity=i.system_capacity,
                                                         timestamp=today).values('dc_power').first()
                try:
                    if ldc_hr_today['dc_power'] < (rdc_hr_today * 80 / 100):
                        all_dc[n] = [ldc_hr_today['dc_power'],rdc_hr_today,rdc_hr_today * 80 / 100,i.id]
                except:
                    continue

        context={'all_dc': all_dc, 'today':today.date()}

        return render(request, 'solarsys/performance_report.html', context)

