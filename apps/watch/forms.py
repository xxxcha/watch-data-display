from django import forms
from .models import Watch,PPG,ECG,Gsensor,Sleep
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
            'freq':"Frequency"
        }

class GsensorCreateForm(forms.ModelForm):
    class Meta:
        model = Gsensor
        fields = ('watch',
                  'acc_x',
                  'acc_y',
                  'acc_z', 
                  'gyr_x',
                  'gyr_y',
                  'gyr_z',
                  'mag_x',
                  'mag_y',
                  'mag_z',
                  'freq')
        labels={
            'freq':"Frequency"
        }

class SleepCreateForm(forms.ModelForm):
    class Meta:
        model = Sleep
        fields = ('watch',
                  'green',
                  'red',
                  'ir', 
                  'x',
                  'y',
                  'z',
                  'sleep_index',
                  'freq')
        labels={
            'sleep_index':"Sleep Index",
            'freq':"Frequency"
        }