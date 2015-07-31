from django.conf.urls import patterns, include, url
from django.contrib import admin

#admin.autodiscover()
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/', 'Masters.views.doc_data',name='docdata'),
    url(r'^druginfo/', 'Masters.views.get_drugdata',name='drugdata'),
    url(r'^docinfo/', 'Masters.views.doctor_data',name='entityinfo'),
    url(r'^pocupdate/', 'Masters.views.poc_update',name='pocupdate'),
    url(r'^gettype/$', 'Masters.views.get_hospital',name='hospital'),
    url(r'^getvillage/$', 'Masters.views.get_uservillage',name='uservillage'),
    url(r'^savehospital/$', 'Masters.views.save_hospital',name='savehospital'),
    url(r'^getvillages/$', 'Masters.views.get_villages',name='hospitalvillages'),
    url(r'^saveusermaintenance/$', 'Masters.views.save_usermaintenance',name='saveusermaintenance'),
    url(r'^updateusermaintenance/$', 'Masters.views.update_usermaintenance',name='editusermaintenance'),
    url(r'^updatehospital/$', 'Masters.views.update_hospitaldetail',name='edithospitals'),

)
