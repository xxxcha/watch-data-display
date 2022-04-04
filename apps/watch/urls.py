# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from .views import HomeView, WatchListView, PPGListView, ECGListView, GsensorListView, SleepListView
from .views import WatchCreateView,WatchDeleteView
from .views import PPGCreateView,PPGDeleteView
from .views import ECGCreateView,ECGDeleteView
from .views import GsensorCreateView,GsensorDeleteView
from .views import SleepCreateView,SleepDeleteView


urlpatterns = [
    # The home page
    path('', HomeView.as_view(), name='home'),

    # Matches any html file
    #re_path(r'^.*\.*', pages, name='pages'),

    path('watch-list',WatchListView.as_view(),name="watch_list"),
    path('watch-create',WatchCreateView.as_view(),name="watch_create"),  
    path('watch-delete/<int:pk>/',WatchDeleteView.as_view(),name="watch_delete"), 
    
    path('ppg-list',PPGListView.as_view(),name="ppg_list"),
    path('ppg-create',PPGCreateView.as_view(),name="ppg_create"),  
    path('ppg-delete/<int:pk>/',PPGDeleteView.as_view(),name="ppg_delete"), 
    
    path('ecg-list',ECGListView.as_view(),name="ecg_list"),
    path('ecg-create',ECGCreateView.as_view(),name="ecg_create"),  
    path('ecg-delete/<int:pk>/',ECGDeleteView.as_view(),name="ecg_delete"), 

    path('gsensor-list',GsensorListView.as_view(),name="gsensor_list"),
    path('gsensor-create',GsensorCreateView.as_view(),name="gsensor_create"),  
    path('gsensor-delete/<int:pk>/',GsensorDeleteView.as_view(),name="gsensor_delete"), 

    path('sleep-list',SleepListView.as_view(),name="sleep_list"),
    path('sleep-create',SleepCreateView.as_view(),name="sleep_create"),  
    path('sleep-delete/<int:pk>/',SleepDeleteView.as_view(),name="sleep_delete"), 


]