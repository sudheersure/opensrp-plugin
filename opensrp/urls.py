from django.conf.urls import patterns, include, url
from django.contrib import admin

#admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'opensrp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/', 'Masters.views.doc_data',name='docdata'),
    url(r'^serviceprovider/', 'Masters.views.service_provider',name='service_provider'),
    #url(r'^serviceprovidertype/', 'UserDetails.views.get_data',name='get_data'),
    url(r'^druginfo/', 'Masters.views.get_drugdata',name='drugdata'),
    # url(r'^diagnosis/', 'UserDetails.views.get_diagnosisdata',name='diagnosisdata'),
    # url(r'^investigationinfo/', 'UserDetails.views.get_investigation',name='investigationinfo'),
    url(r'^pocinfo/', 'Masters.views.poc_data',name='pocinfo'),
    url(r'^docinfo/', 'Masters.views.doctor_data',name='entityinfo'),
    #url(r'^pocsave/', 'UserDetails.views.poc_save',name='pocsave'),
    url(r'^pocupdate/', 'Masters.views.poc_update',name='pocupdate'),
)
