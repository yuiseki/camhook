from django.db import models
from django.contrib import admin

from django.db.models.signals import post_save
from django.contrib.auth.models import User


"""
class Tweet(models.Model):
    user = models.ForeignKey(User)
    tweet_id = models.CharField(max_length=20)
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField()
    lng = models.FloatField()
    lat = models.FloatField()
"""


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    access_token = models.CharField(max_length=255, blank=True, null=True, editable=False)
    profile_image_url = models.CharField(max_length=4095, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=4095, blank=True, null=True)
    description = models.CharField(max_length=160, blank=True, null=True)

    def __str__(self):
        return "%s's profile" % self.user

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)



try:
    admin.site.register(UserProfile)
except:
    pass
