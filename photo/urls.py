from django.conf.urls.defaults import *

urlpatterns = patterns('camhook.photo.views',
    url(r'create',  'create',  name='photo_create'),
    url(r'^update/(?P<title>[-\w]+)$',  'update',  name='photo_update'),

    url(r'^(?P<title>[-\w]+)/?$',  'thread',  name='photo_thread'),

    url(r'',  'top',  name='photo_top'),
)
