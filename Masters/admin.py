from django.contrib import admin
from Masters.models import *
from django.http import HttpResponse
from Masters.forms import *


class DimAnmAdmin(admin.ModelAdmin):
    list_display = ('anmidentifier','phc','subcenter','name',)
    search_fields = ('anmidentifier','phc__name','subcenter','name',)
    list_filter = ('phc','subcenter',)

class DimIndicatorAdmin(admin.ModelAdmin):
    list_display = ('indicator',)
    list_filter = ('indicator',)

class DimLocationAdmin(admin.ModelAdmin):
    list_display = ('village','subcenter','phc','taluka','district','state',)
    def has_add_permission(self, request):
        return False

class DimPhcAdmin(admin.ModelAdmin):
    list_display = ('phcidentifier','name',)

    def has_add_permission(self, request):
        return False

class DimServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('service_provider','type',)

    def has_add_permission(self, request):
        return False


class DimServiceProviderTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)

    def has_add_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        self.list_display_links = (None, )
        return super(DimServiceProviderTypeAdmin, self).changelist_view(request, extra_context=None)

class DimUserLoginAdmin(admin.ModelAdmin):
    form = UserInfoForm
    list_display = ('name','user_role',)



class DrugInfoAdmin(admin.ModelAdmin):
    
    list_display= ('drug_name','frequency','dosage','direction',)
    search_fields = ('drug_name',)

            
class FrequencyAdmin(admin.ModelAdmin):
    
    list_display = ('number_of_times','active',)
    list_filter = ('active',)

    def get_actions(self, request):
        actions = super(FrequencyAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

class DosageAdmin(admin.ModelAdmin):
    list_display = ('dosage','active',)
    def get_actions(self, request):
        actions = super(DosageAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

class DirectionsAdmin(admin.ModelAdmin):
    list_display = ('directions','active',)
    def get_actions(self, request):
        actions = super(DirectionsAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

class ICD10Admin(admin.ModelAdmin): 
    list_display = ('ICD10_Chapter','ICD10_Code','ICD10_Name','can_select','status')

class InvestigationAdmin(admin.ModelAdmin):
    list_display = ('service_group_name','investigation_name','is_active',)

class PocInfoAdmin(admin.ModelAdmin):
    list_display = ('visitentityid','entityidec','anmid','level','clientversion','serverversion','visittype','phc',)

class DocInfoAdmin(admin.ModelAdmin):
    list_display= ('docname','phc',)


admin.site.register(DimAnm,DimAnmAdmin)
admin.site.register(DimIndicator,DimIndicatorAdmin)
admin.site.register(DimLocation,DimLocationAdmin)
admin.site.register(DimPhc,DimPhcAdmin)
admin.site.register(DimServiceProvider,DimServiceProviderAdmin)
admin.site.register(DimServiceProviderType,DimServiceProviderTypeAdmin)
admin.site.register(DimUserLogin,DimUserLoginAdmin)
admin.site.register(DrugInfo,DrugInfoAdmin)
admin.site.register(Frequency,FrequencyAdmin)
admin.site.register(Dosage,DosageAdmin)
admin.site.register(Directions,DirectionsAdmin)
admin.site.register(ICD10,ICD10Admin)
admin.site.register(Investigations,InvestigationAdmin)
admin.site.register(PocInfo,PocInfoAdmin)
admin.site.register(DocInfo,DocInfoAdmin)
