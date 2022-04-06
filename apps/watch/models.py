# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.urls import reverse

# Create your models here.
class Watch(models.Model):
    name = models.CharField(max_length=20)
    mac = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    def get_absolute_url(self): 
        return reverse('watch_list')

class PPG(models.Model):
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE, related_name='watch1')
    green = models.FloatField(blank=True,null=True)
    red = models.FloatField(blank=True,null=True)
    ir = models.FloatField(blank=True,null=True)
    freq = models.IntegerField()
    created = models.DateTimeField(auto_now=True)

    def get_absolute_url(self): 
        return reverse('ppg_list')
 
 
class ECG(models.Model):
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE, related_name='watch2')
    ecg = models.FloatField(blank=True,null=True)
    mv = models.FloatField(blank=True,null=True)
    freq = models.IntegerField()
    created = models.DateTimeField(auto_now=True)  

    def get_absolute_url(self): 
        return reverse('ecg_list')
 
 
class Gsensor(models.Model):
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE, related_name='watch3')
    acc_x = models.FloatField(blank=True,null=True)
    acc_y = models.FloatField(blank=True,null=True)
    acc_z = models.FloatField(blank=True,null=True)
    gyr_x = models.FloatField(blank=True,null=True)
    gyr_y = models.FloatField(blank=True,null=True)
    gyr_z = models.FloatField(blank=True,null=True)
    mag_x = models.FloatField(blank=True,null=True)
    mag_y = models.FloatField(blank=True,null=True)
    mag_z = models.FloatField(blank=True,null=True)
    freq = models.IntegerField()
    created = models.DateTimeField(auto_now=True)

    def get_absolute_url(self): 
        return reverse('gsensor_list')

class Sleep(models.Model):
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE, related_name='watch4')
    green = models.FloatField(blank=True,null=True)
    red = models.FloatField(blank=True,null=True)
    ir = models.FloatField(blank=True,null=True)
    x = models.FloatField(blank=True,null=True)
    y = models.FloatField(blank=True,null=True)
    z = models.FloatField(blank=True,null=True)
    sleep_index = models.IntegerField(blank=True,null=True)
    freq = models.IntegerField()
    created = models.DateTimeField(auto_now=True)

    def get_absolute_url(self): 
        return reverse('sleep_list')

