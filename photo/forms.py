# -*- coding: utf-8 -*-
from django import forms
from photo.models import Thread

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
