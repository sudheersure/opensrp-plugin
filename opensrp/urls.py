from django.conf.urls import patterns, include, url
from django.contrib import admin

#admin.autodiscover()
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/', 'Masters.views.doc_data',name='docdata'),
    url(r'^druginfo/', 'Masters.views.get_drugdata',name='drugdata'),
    url(r'^docinfo/', 'Masters.views.doctor_data',name='entityinfo'),
    url(r'^pocupdate/', 'Masters.views.poc_update',name='pocupdate'),
)
