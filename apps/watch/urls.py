# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from .views import HomeView, WatchListView, PPGListView, ECGListView, ACCListView, GYRListView
from .views import WatchCreateView,WatchDeleteView
from .views import PPGCreateView,PPGDeleteView,PPGChartView
from .views import ECGCreateView,ECGDeleteView,ECGChartView
from .views import ACCCreateView,ACCDeleteView,ACCChartView
from .views import GYRCreateView,GYRDeleteView,GYRChartView


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
    path('ppg-chart',PPGChartView.as_view(),name="ppg_chart"),
    
    path('ecg-list',ECGListView.as_view(),name="ecg_list"),
    path('ecg-create',ECGCreateView.as_view(),name="ecg_create"),  
    path('ecg-delete/<int:pk>/',ECGDeleteView.as_view(),name="ecg_delete"), 
    path('ecg-chart',ECGChartView.as_view(),name="ecg_chart"),

    path('acc-list',ACCListView.as_view(),name="acc_list"),
    path('acc-create',ACCCreateView.as_view(),name="acc_create"),  
    path('acc-delete/<int:pk>/',ACCDeleteView.as_view(),name="acc_delete"),
    path('acc-chart',ACCChartView.as_view(),name="acc_chart"), 

    path('gyr-list',GYRListView.as_view(),name="gyr_list"),
    path('gyr-create',GYRCreateView.as_view(),name="gyr_create"),  
    path('gyr-delete/<int:pk>/',GYRDeleteView.as_view(),name="gyr_delete"), 
    path('gyr-chart',GYRChartView.as_view(),name="gyr_chart"),


]