from django.contrib import admin
from Masters.models import *
from django.http import HttpResponse
from Masters.forms import *


class DimAnmAdmin(admin.ModelAdmin):
    list_display = ('anmidentifier','phc','subcenter','name',)
    search_fields = ('anmidentifier','phc__name','subcenter','name',)
    list_filter = ('phc','subcenter',)

    def get_actions(self, request):
        actions = super(DimAnmAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class DimIndicatorAdmin(admin.ModelAdmin):
    list_display = ('indicator',)
    list_filter = ('indicator','active',)
    search_fields = ('indicator','active',)

    def get_actions(self, request):
        actions = super(DimIndicatorAdmin   , self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class DimLocationAdmin(admin.ModelAdmin):
    list_display = ('village','subcenter','phc','taluka','district','state',)
    search_fields = ('village','subcenter','phc__name','taluka','district','state','active',)
    list_filter = ('village','subcenter',)

    def get_actions(self, request):
        actions = super(DimLocationAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions
    
    def has_delete_permission(self, request, obj=None):
        return False

class DimPhcAdmin(admin.ModelAdmin):
    list_display = ('phcidentifier','name',)
    search_fields = ('phcidentifier','name','active',)
    list_filter = ('name',)

    def get_actions(self, request):
        actions = super(DimPhcAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class DimServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('service_provider','type',)
    search_fields = ('service_provider','type__type','active',)
    list_filter = ('type',)

    def get_actions(self, request):
        actions = super(DimServiceProviderAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False 


class DimServiceProviderTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)
    search_fields = ('type','active',)
    list_filter = ('type',)

    def get_actions(self, request):
        actions = super(DimServiceProviderTypeAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        self.list_display_links = (None, )
        return super(DimServiceProviderTypeAdmin, self).changelist_view(request, extra_context=None)

class DimUserLoginAdmin(admin.ModelAdmin):
    form = UserInfoForm
    list_display = ('name','user_role',)
    search_fields = ('name','user_role__type','active',)
    list_filter = ('name','user_role',)

    def get_actions(self, request):
        actions = super(DimUserLoginAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class DrugInfoAdmin(admin.ModelAdmin):
    list_display= ('drug_name','frequency','dosage','direction',)
    search_fields = ('drug_name','frequency__number_of_times','dosage__dosage','direction__directions','active',)
    list_filter = ('drug_name',)

    def get_actions(self, request):
        actions = super(DrugInfoAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

            
class FrequencyAdmin(admin.ModelAdmin):
    list_display = ('number_of_times','active',)
    list_filter = ('active',)
    search_fields = ('number_of_times','active',)

    def get_actions(self, request):
        actions = super(FrequencyAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class DosageAdmin(admin.ModelAdmin):
    list_display = ('dosage','active',)
    search_fields = ('dosage','active')
    list_filter = ('dosage',)

    def get_actions(self, request):
        actions = super(DosageAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


class DirectionsAdmin(admin.ModelAdmin):
    list_display = ('directions','active',)
    search_fields = ('directions','active',)
    list_filter = ('directions',)

    def get_actions(self, request):
        actions = super(DirectionsAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class ICD10Admin(admin.ModelAdmin): 
    list_display = ('ICD10_Chapter','ICD10_Code','ICD10_Name','can_select','status')
    search_fields = ('ICD10_Chapter','ICD10_Code','ICD10_Name','can_select','status','active',)
    list_filter = ('ICD10_Code','ICD10_Chapter','ICD10_Name',)

    def get_actions(self, request):
        actions = super(ICD10Admin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class InvestigationAdmin(admin.ModelAdmin):
    list_display = ('service_group_name','investigation_name','is_active',)
    search_fields = ('service_group_name','investigation_name','is_active',)
    list_filter = ('service_group_name',)

    def get_actions(self, request):
        actions = super(InvestigationAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class PocInfoAdmin(admin.ModelAdmin):    
    list_display = ('visitentityid','entityidec','anmid','level','clientversion','serverversion','visittype','phc','active',)
    search_fields = ('visitentityid','entityidec','anmid','level','clientversion','serverversion','visittype','phc','active',)
    list_filter = ('anmid','level','clientversion','serverversion','phc')

    def get_actions(self, request):
        actions = super(PocInfoAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class DocInfoAdmin(admin.ModelAdmin):
    list_display= ('docname','phc',)
    search_fields = ('docname','phc__name','active')
    list_filter = ('docname','phc__name',)

    def get_actions(self, request):
        actions = super(DocInfoAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False
        

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
