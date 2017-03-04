from django.contrib import admin

# Register your models here.
from django.contrib import admin, messages
from .models import Reference, InstallationKey, LiveDC
import utilities

# admin.ModelAdmin customizes default model class when using admin.site.register

class ReferenceAdmin(admin.ModelAdmin):
    model = Reference
    fields = ['lat', 'long', 'system_capacity']
    list_display = ('lat', 'long', 'system_capacity','dc')
    list_filter = ['lat', 'long', 'system_capacity']
    search_fields = ['id']

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
    fields = ['lat', 'long', 'system_capacity']
    list_display = ['lat', 'long', 'system_capacity']
    list_filter = ['lat', 'long', 'system_capacity']
    search_fields = ['installation_key']


class LiveDCAdmin(admin.ModelAdmin):
    model = LiveDC
    list_display = ['installation_key', 'timestamp', 'dc_power']


admin.site.register(Reference, ReferenceAdmin)
admin.site.register(InstallationKey, InstallationKeyAdmin)
admin.site.register(LiveDC, LiveDCAdmin)