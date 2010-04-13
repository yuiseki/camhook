from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/?(.*)', admin.site.root),
    (r'^twitter/', include('camhook.twitterauth.urls')),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
       {'document_root': 'media_root'}),

    (r'', include('camhook.photo.urls')),

)
