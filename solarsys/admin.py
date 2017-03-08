from django.contrib import admin

# Register your models here.
from django.contrib import admin, messages
from haversine import haversine
from .models import Reference, InstallationKey, LiveDC
import utilities

# admin.ModelAdmin customizes default model class when using admin.site.register

class ReferenceAdmin(admin.ModelAdmin):
    model = Reference
    fields = ['lat', 'long', 'system_capacity']
    list_display = ['id','lat', 'long', 'system_capacity','dc', 'added_on']
    list_filter = ['lat', 'long', 'system_capacity', 'added_on']
    search_fields = ['id', 'added_on']

    def save_model(self, request, obj, form, change):
        try:    #find existing Reference object
            ref = Reference.objects.get(lat=form.cleaned_data['lat'],long=form.cleaned_data['long'],
                    system_capacity=form.cleaned_data['system_capacity'])
            messages.set_level(request, messages.ERROR)
            messages.error(request,"Object ID: %d, with given lat/lon/sc already exists!" %ref.id)

        except:
            util_rt = utilities.getRefDC_API(form.cleaned_data['lat'], form.cleaned_data['long'],
                                  form.cleaned_data['system_capacity'])
            if isinstance(util_rt,str):
                messages.set_level(request, messages.ERROR)
                messages.error (request, util_rt)
            else:
                obj.dc = util_rt
                super(ReferenceAdmin, self).save_model(request, obj, form, change)


class InstallationKeyAdmin(admin.ModelAdmin):
    model = InstallationKey
    fields = ['lat', 'long', 'system_capacity','address']
    list_display = ['installation_key', 'lat', 'long', 'system_capacity','installation_id','address','added_on']
    list_filter = ['lat', 'long', 'system_capacity', 'installation_id', 'added_on']
    search_fields = ['installation_key', 'added_on']

    def save_model(self, request, obj, form, change):
        ik_lat = form.cleaned_data['lat']
        ik_long = form.cleaned_data['long']
        ik_sc = form.cleaned_data['system_capacity']
        try:    #find existing IK object
            ik = InstallationKey.objects.get(lat=ik_lat,long=ik_long, system_capacity=ik_sc)
            if not change:
                messages.set_level(request, messages.ERROR)
                messages.error(request,"An InstallationKey: {ik}, with given lat/lon/sc already exists!".format(ik=ik.installation_key))
            elif ik.installation_key <> obj.installation_key:
                messages.set_level(request, messages.ERROR)
                messages.error(request,
                            "Another InstallationKey: {ik}, with given lat/lon/sc already exists!".format(ik=ik.installation_key))
            else:
                raise Exception
        except:
            try:
                refid = utilities.nearest_point(ik_lat, ik_long, ik_sc)
                ref = Reference.objects.get(id=refid) if refid else None
                if haversine((ik_lat, ik_long), (ref.lat, ref.long)) <=1:  #if ref object found in 1km radius
                        obj.installation_id = ref
                else:
                    raise Exception
            except:
                refdc = utilities.getRefDC_API(ik_lat,ik_long,ik_sc)
                if isinstance(refdc,str):
                    messages.set_level(request, messages.ERROR)
                    messages.error(request, refdc)
                else:
                    ref, created = Reference.objects.update_or_create(lat=ik_lat, long=long, system_capacity=ik_sc,
                                                                      defaults={'dc': refdc})
                    obj.installation_id = ref
            super(InstallationKeyAdmin, self).save_model(request, obj, form, change)


class LiveDCAdmin(admin.ModelAdmin):
    model = LiveDC
    list_display = ['installation_key', 'timestamp', 'dc_power']


admin.site.register(Reference, ReferenceAdmin)
admin.site.register(InstallationKey, InstallationKeyAdmin)
admin.site.register(LiveDC, LiveDCAdmin)