from django.conf.urls.defaults import *


urlpatterns = patterns('camhook.twitterauth.views',
    url(r'^login$', 'twitter_signin', name='login'),
    url(r'^return.*', 'twitter_return', name='return'),
)


