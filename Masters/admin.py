from django.contrib import admin
from Masters.models import *
from django.http import HttpResponse
from Masters.forms import *
from django.conf.urls import patterns, url
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.shortcuts import render
from collections import defaultdict

class DimAnmAdmin(admin.ModelAdmin):
    list_display = ('anmidentifier','phc','subcenter','name',)
    search_fields = ('anmidentifier','phc__name',)

    def get_actions(self, request):
        actions = super(DimAnmAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class DimIndicatorAdmin(admin.ModelAdmin):
    list_display = ('indicator',)
    search_fields = ('indicator',)

    def get_actions(self, request):
        actions = super(DimIndicatorAdmin   , self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class DimPhcAdmin(admin.ModelAdmin):
    list_display = ('phcidentifier','name',)
    search_fields = ('phcidentifier','name',)

    def get_actions(self, request):
        actions = super(DimPhcAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class DimServiceProviderAdmin(admin.ModelAdmin):
    list_display = ('service_provider','type',)
    search_fields = ('service_provider','type__type',)

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
    search_fields = ('type',)

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
    search_fields = ('name','user_role__type',)

    def get_actions(self, request):
        actions = super(DimUserLoginAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class DrugInfoAdmin(admin.ModelAdmin):
    list_display= ('drug_name','frequency','dosage','direction','active',)
    search_fields = ('drug_name',)

    def get_actions(self, request):
        actions = super(DrugInfoAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

            
class FrequencyAdmin(admin.ModelAdmin):
    list_display = ('number_of_times','active',)
    search_fields = ('number_of_times',)

    def get_actions(self, request):
        actions = super(FrequencyAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class DosageAdmin(admin.ModelAdmin):
    list_display = ('dosage','active',)
    search_fields = ('dosage',)

    def get_actions(self, request):
        actions = super(DosageAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


class DirectionsAdmin(admin.ModelAdmin):
    list_display = ('directions','active',)
    search_fields = ('directions',)

    def get_actions(self, request):
        actions = super(DirectionsAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class ICD10Admin(admin.ModelAdmin): 
    list_display = ('ICD10_Chapter','ICD10_Code','ICD10_Name','can_select','status')
    search_fields = ('ICD10_Chapter','ICD10_Code','ICD10_Name',)

    def get_actions(self, request):
        actions = super(ICD10Admin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class InvestigationAdmin(admin.ModelAdmin):
    list_display = ('service_group_name','investigation_name','is_active',)
    search_fields = ('service_group_name','investigation_name','is_active',)

    def get_actions(self, request):
        actions = super(InvestigationAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class PocInfoAdmin(admin.ModelAdmin):    
    list_display = ('visitentityid','entityidec','anmid','level','clientversion','serverversion','visittype','phc','pending','docid',)
    search_fields = ('visitentityid','entityidec','anmid',)

    def get_actions(self, request):
        actions = super(PocInfoAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class DocInfoAdmin(admin.ModelAdmin):
    list_display= ('docname','phc',)
    search_fields = ('docname',)

    def get_actions(self, request):
        actions = super(DocInfoAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False
        
class UserMaintenanceAdmin(admin.ModelAdmin):
    form = UserMaintenaceForm
    list_display = ('user_id','user_role','name','phone_number','email','country','county','district','subdistrict','subcenter','hospital','villages','active')
    search_fields = ('user_id',)

    def get_urls(self):
        urls = super(UserMaintenanceAdmin, self).get_urls()
        my_urls = patterns('',
                url(r'add/$', 'Masters.views.adminadd_usermaintenance',name='user_maintenance'),
                

                url(r'(?P<batch_id>\d+)/$','Masters.views.edit_usermaintenance',name='editusermaintenance'),
                )
        
        return my_urls + urls

    def get_actions(self, request):
        actions = super(UserMaintenanceAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class CountryAdmin(admin.ModelAdmin):
    list_display=('country_name','country_code','active',)
    search_fields = ('country_name',)

    def get_actions(self, request):
        actions = super(CountryAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class CountyAdmin(admin.ModelAdmin):
    list_display = ('county_name','country_name','active',)
    search_fields = ('county_name',)

    def get_actions(self, request):
        actions = super(CountyAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class DisttabAdmin(admin.ModelAdmin):
    list_display = ('district_name','county_name','country_name','active')
    search_fields = ('district_name',)

    def get_urls(self):
        urls = super(DisttabAdmin, self).get_urls()
        my_urls = patterns('',
                url(r'add/$', 'Masters.views.adminadd_district',name='add_district'),


                url(r'(?P<district_id>\d+)/$','Masters.views.edit_district',name='editdistrict'),
                )
        return my_urls + urls

    def get_actions(self, request):
        actions = super(DisttabAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class SubdistrictTabAdmin(admin.ModelAdmin):
    list_display = ('subdistrict','district','county','country','active',)
    search_fields = ('subdistrict',)

    def get_urls(self):
        urls = super(SubdistrictTabAdmin, self).get_urls()
        my_urls = patterns('',
                url(r'add/$', 'Masters.views.adminadd_subdistrict',name='add_subdistrict'),


                url(r'(?P<subdistrict_id>\d+)/$','Masters.views.edit_subdistrict',name='editsubdistrict'),
                )
        return my_urls + urls

    def get_actions(self, request):
        actions = super(SubdistrictTabAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class LocationTabAdmin(admin.ModelAdmin):
    list_display = ('location','subdistrict','district','county','country','active',)
    search_fields = ('location',)

    def get_urls(self):
        urls = super(LocationTabAdmin, self).get_urls()
        my_urls = patterns('',
                url(r'add/$', 'Masters.views.adminadd_location',name='add_subdistrict'),


                url(r'(?P<loc_id>\d+)/$','Masters.views.edit_location',name='editlocation'),
                )
        return my_urls + urls

    def get_actions(self, request):
        actions = super(LocationTabAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


class HealthCenterAdmin(admin.ModelAdmin):
    list_display = ('hospital_name','hospital_type','hospital_address','country_name','county_name','district_name','subdistrict_name','parent_hospital','villages','active')
    search_fields = ('hospital_name',)

    def get_urls(self):
        urls = super(HealthCenterAdmin, self).get_urls()
        my_urls = patterns('',
                url(r'add/$', 'Masters.views.admin_hospital',name='hospital'),
                url(r'gettype/$', 'Masters.views.get_hospital',name='hospital'),
                url(r'(?P<hospital_id>\d+)/$', 'Masters.views.edit_hospital',name='edithospital'),
                )
        return my_urls + urls

    def get_actions(self, request):
        actions = super(HealthCenterAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class AppConfigurationAdmin(admin.ModelAdmin):
    list_display = ('wife_age_min','wife_age_max','husband_age_min','husband_age_max','temperature_units','country_name',)
    search_fields = ('wife_age_min',)
    fieldsets = (
      (None, {
          'fields': ('country_name','temperature_units','registration_text','poc_text','escalation_schedule')
      }),
      ('Wife age', {
          'fields': ('wife_age_min','wife_age_max')
      }),
      ('Husband age', {
          'fields': ('husband_age_min','husband_age_max')
      }),

   )

    def get_actions(self, request):
        actions = super(AppConfigurationAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

class FormFieldsAdmin(admin.ModelAdmin):
    list_display = ("form_name","country","field1","field2","field3","field4","field5")

    def get_actions(self, request):
        actions = super(FormFieldsAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(DimAnm,DimAnmAdmin)
admin.site.register(DimPhc,DimPhcAdmin)
admin.site.register(DrugInfo,DrugInfoAdmin)
admin.site.register(Frequency,FrequencyAdmin)
admin.site.register(Dosage,DosageAdmin)
admin.site.register(Directions,DirectionsAdmin)
admin.site.register(ICD10,ICD10Admin)
admin.site.register(Investigations,InvestigationAdmin)
admin.site.register(PocInfo,PocInfoAdmin)
admin.site.register(UserMasters,UserMaintenanceAdmin)
admin.site.register(CountryTb,CountryAdmin)
admin.site.register(CountyTb,CountyAdmin)
admin.site.register(Disttab,DisttabAdmin)
admin.site.register(SubdistrictTab,SubdistrictTabAdmin)
admin.site.register(LocationTab,LocationTabAdmin)
admin.site.register(HealthCenters,HealthCenterAdmin)
admin.site.register(AppConfiguration,AppConfigurationAdmin)
admin.site.register(FormFields,FormFieldsAdmin)