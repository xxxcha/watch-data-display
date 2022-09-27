# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.urls import reverse
from datetime import datetime

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
    index = models.IntegerField(default=0)
    created = models.DateTimeField(default=datetime.now())

    def get_absolute_url(self): 
        return reverse('ppg_list')
 
 
class ECG(models.Model):
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE, related_name='watch2')
    ecg = models.FloatField(blank=True,null=True)
    mv = models.FloatField(blank=True,null=True)
    freq = models.IntegerField()
    index = models.IntegerField(default=0)
    created = models.DateTimeField(default=datetime.now())  

    def get_absolute_url(self): 
        return reverse('ecg_list')
 
class ACC(models.Model):
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE, related_name='watch3')
    x = models.FloatField(blank=True,null=True)
    y = models.FloatField(blank=True,null=True)
    z = models.FloatField(blank=True,null=True)
    freq = models.IntegerField()
    index = models.IntegerField(default=0)
    created = models.DateTimeField(default=datetime.now())

    def get_absolute_url(self): 
        return reverse('acc_list')

class GYR(models.Model):
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE, related_name='watch4')
    x = models.FloatField(blank=True,null=True)
    y = models.FloatField(blank=True,null=True)
    z = models.FloatField(blank=True,null=True)
    freq = models.IntegerField()
    index = models.IntegerField(default=0)
    created = models.DateTimeField(default=datetime.now())

    def get_absolute_url(self): 
        return reverse('gyr_list')


