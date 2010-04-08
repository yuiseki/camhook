from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/?(.*)', admin.site.root),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
       {'document_root': 'media_root'}),


    (r'', include('camhook.photo.urls')),
)
