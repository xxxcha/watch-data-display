from django import forms
from .models import Watch,PPG,ECG,ACC,GYR
from django.contrib import admin
from django.urls import reverse


class WatchCreateForm(forms.ModelForm):
    class Meta:
        model = Watch
        fields = ('name',
                  'mac')
        labels={
            'mac':'MAC Address'
        }

class PPGCreateForm(forms.ModelForm):
    class Meta:
        model = PPG
        fields = ('watch',
                  'green',
                  'red',
                  'ir', 
                  'freq')
        labels={
            'ir':'IR',
            'freq':"Frequency"
        }

class ECGCreateForm(forms.ModelForm):
    class Meta:
        model = ECG
        fields = ('watch',
                  'ecg',
                  'mv',
                  'freq')
        labels={
            'ecg': "ECG Value",
            'mv': "MV Value",
            'freq':"Frequency"
        }

class ACCCreateForm(forms.ModelForm):
    class Meta:
        model = ACC
        fields = ('watch',
                  'x',
                  'y',
                  'z', 
                  'freq')
        labels={
            'freq':"Frequency"
        }

class GYRCreateForm(forms.ModelForm):
    class Meta:
        model = GYR
        fields = ('watch',
                  'x',
                  'y',
                  'z',
                  'freq')
        labels={
            'freq':"Frequency"
        }