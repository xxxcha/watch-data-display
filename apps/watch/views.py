# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import ListView,View,TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Sum, Count
from datetime import date,timedelta,datetime
from .models import Watch, PPG, ECG, Gsensor, Sleep
from django.contrib.messages.views import messages
from .forms import WatchCreateForm,PPGCreateForm,ECGCreateForm,GsensorCreateForm,SleepCreateForm


PAGINATOR_NUMBER = 5

class HomeView(LoginRequiredMixin,TemplateView):
    login_url = 'login'
    template_name = "index.html"
    context={}

    def get(self,request, *args, **kwargs):

        watch_count = Watch.objects.all().count()
        
        data_count = {"ppg":PPG.objects.all().count(),
                    "ecg":ECG.objects.all().count(),
                    "gsensor":Gsensor.objects.all().count(),
                    "sleep":Sleep.objects.all().count()}
        all_count=data_count['ppg']+data_count['ecg']+data_count['gsensor']+data_count['sleep']       
        
        current_week = date.today().isocalendar()[1]
        
        self.context['watch_count']=watch_count
        self.context['data_count']=data_count
        self.context['all_count']=all_count

        return render(request, self.template_name, self.context)

class WatchListView(LoginRequiredMixin,ListView):
    login_url = 'login'
    model=Watch
    context_object_name = 'watch_list'
    template_name = 'watch/Watch.html'
    order_field = 'name'
    search_value=""

    def get_queryset(self):
        search =self.request.GET.get("search") 
        order_by=self.request.GET.get("orderby")

        if order_by:
            all_watch = Watch.objects.all().order_by(order_by)
            self.order_field=order_by
        else:
            all_watch = Watch.objects.all().order_by(self.order_field)

        if search:
            all_watch = all_watch.filter(
                Q(name__icontains=search)
            )
            self.search_value=search

        self.count_total = all_watch.count()
        paginator = Paginator(all_watch, PAGINATOR_NUMBER)
        page = self.request.GET.get('page')
        watch = paginator.get_page(page)

        return watch

    def get_context_data(self, *args, **kwargs):
        context = super(WatchListView, self).get_context_data(*args, **kwargs)
        context['count_total'] = self.count_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['page_objects'] = self.get_queryset()
        return context

class WatchCreateView(LoginRequiredMixin,CreateView):
    model=Watch
    login_url = 'login'
    form_class=WatchCreateForm    
    template_name='watch/Watch_create.html'

    def post(self,request, *args, **kwargs):
        super(WatchCreateView,self).post(request)
        new_watch_name = request.POST['name']
        messages.success(request, f"New watch << {new_watch_name} >> Added")
        return redirect('watch_list')

class WatchDeleteView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request,*args,**kwargs):
        watch_pk=kwargs["pk"]
        delete_watch=Watch.objects.get(pk=watch_pk)
        #model_name = delete_watch.__class__.__name__
        messages.error(request, f"Watch << {delete_watch.name} >> Removed")
        delete_watch.delete()
        
        return HttpResponseRedirect(reverse("watch_list"))

class PPGListView(ListView):
    model=PPG
    context_object_name = 'ppg_list'
    template_name = 'watch/PPG.html'
    order_field = '-created'
    search_value=""

    def get_queryset(self):
        search =self.request.GET.get("search") 
        order_by=self.request.GET.get("orderby")

        if order_by:
            all_ppg = PPG.objects.all().order_by(order_by)
            self.order_field=order_by
        else:
            all_ppg = PPG.objects.all().order_by(self.order_field)

        if search:
            all_ppg = all_ppg.filter(
                Q(watch__name__icontains=search)
            )
            self.search_value=search

        self.count_total = all_ppg.count()
        paginator = Paginator(all_ppg, PAGINATOR_NUMBER)
        page = self.request.GET.get('page')
        ppg = paginator.get_page(page)

        return ppg

    def get_context_data(self, *args, **kwargs):
        context = super(PPGListView, self).get_context_data(*args, **kwargs)
        context['count_total'] = self.count_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['page_objects'] = self.get_queryset()
        return context

class PPGCreateView(LoginRequiredMixin,CreateView):
    model=PPG
    login_url = 'login'
    form_class=PPGCreateForm    
    template_name='watch/PPG_create.html'

    def post(self,request, *args, **kwargs):
        super(PPGCreateView,self).post(request)
        messages.success(request, f"This PPG Item Added")
        return redirect('ppg_list')

class PPGDeleteView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request,*args,**kwargs):
        ppg_pk=kwargs["pk"]
        delete_ppg=PPG.objects.get(pk=ppg_pk)       
        messages.error(request, f"This PPG Item Removed")
        delete_ppg.delete()
        
        return HttpResponseRedirect(reverse("ppg_list"))


class ECGListView(ListView):
    model=ECG
    context_object_name = 'ecg_list'
    template_name = 'watch/ECG.html'
    order_field = '-created'
    search_value=""

    def get_queryset(self):
        search =self.request.GET.get("search") 
        order_by=self.request.GET.get("orderby")

        if order_by:
            all_ecg = ECG.objects.all().order_by(order_by)
            self.order_field=order_by
        else:
            all_ecg = ECG.objects.all().order_by(self.order_field)

        if search:
            all_ecg = all_ecg.filter(
                Q(watch__name__icontains=search)
            )
            self.search_value=search

        self.count_total = all_ecg.count()
        paginator = Paginator(all_ecg, PAGINATOR_NUMBER)
        page = self.request.GET.get('page')
        ecg = paginator.get_page(page)
        return ecg

    def get_context_data(self, *args, **kwargs):
        context = super(ECGListView, self).get_context_data(*args, **kwargs)
        context['count_total'] = self.count_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['page_objects'] = self.get_queryset()
        return context

class ECGCreateView(LoginRequiredMixin,CreateView):
    model=ECG
    login_url = 'login'
    form_class=ECGCreateForm    
    template_name='watch/ECG_create.html'

    def post(self,request, *args, **kwargs):
        super(ECGCreateView,self).post(request)
        messages.success(request, f"This ECG Item Added")
        return redirect('ecg_list')

class ECGDeleteView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request,*args,**kwargs):
        ecg_pk=kwargs["pk"]
        delete_ecg=ECG.objects.get(pk=ecg_pk)       
        messages.error(request, f"This ECG Item Removed")
        delete_ecg.delete()
        
        return HttpResponseRedirect(reverse("ecg_list"))


class GsensorListView(ListView):
    model=Gsensor
    context_object_name = 'gsensor_list'
    template_name = 'watch/Gsensor.html'
    order_field = '-created'
    search_value=""

    def get_queryset(self):
        search =self.request.GET.get("search") 
        order_by=self.request.GET.get("orderby")

        if order_by:
            all_gsensor = Gsensor.objects.all().order_by(order_by)
            self.order_field=order_by
        else:
            all_gsensor = Gsensor.objects.all().order_by(self.order_field)

        if search:
            all_gsensor = all_gsensor.filter(
                Q(watch__name__icontains=search)
            )
            self.search_value=search

        self.count_total = all_gsensor.count()
        paginator = Paginator(all_gsensor, PAGINATOR_NUMBER)
        page = self.request.GET.get('page')
        gsensor = paginator.get_page(page)
        return gsensor

    def get_context_data(self, *args, **kwargs):
        context = super(GsensorListView, self).get_context_data(*args, **kwargs)
        context['count_total'] = self.count_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['page_objects'] = self.get_queryset()
        return context

class GsensorCreateView(LoginRequiredMixin,CreateView):
    model=Gsensor
    login_url = 'login'
    form_class=GsensorCreateForm    
    template_name='watch/Gsensor_create.html'

    def post(self,request, *args, **kwargs):
        super(GsensorCreateView,self).post(request)
        messages.success(request, f"This Gsensor Item Added")
        return redirect('gsensor_list')

class GsensorDeleteView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request,*args,**kwargs):
        gsensor_pk=kwargs["pk"]
        delete_gsensor=Gsensor.objects.get(pk=gsensor_pk)       
        messages.error(request, f"This Gsensor Item Removed")
        delete_gsensor.delete()
        
        return HttpResponseRedirect(reverse("gsensor_list"))

class SleepListView(ListView):
    model=Sleep
    context_object_name = 'sleep_list'
    template_name = 'watch/Sleep.html'
    order_field = '-created'
    search_value=""

    def get_queryset(self):
        search =self.request.GET.get("search") 
        order_by=self.request.GET.get("orderby")

        if order_by:
            all_sleep = Sleep.objects.all().order_by(order_by)
            self.order_field=order_by
        else:
            all_sleep = Sleep.objects.all().order_by(self.order_field)

        if search:
            all_sleep = all_sleep.filter(
                Q(watch__name__icontains=search)
            )
            self.search_value=search

        self.count_total = all_sleep.count()
        paginator = Paginator(all_sleep, PAGINATOR_NUMBER)
        page = self.request.GET.get('page')
        sleep = paginator.get_page(page)
        return sleep

    def get_context_data(self, *args, **kwargs):
        context = super(SleepListView, self).get_context_data(*args, **kwargs)
        context['count_total'] = self.count_total
        context['search'] = self.search_value
        context['orderby'] = self.order_field
        context['page_objects'] = self.get_queryset()
        return context

class SleepCreateView(LoginRequiredMixin,CreateView):
    model=Sleep
    login_url = 'login'
    form_class=SleepCreateForm    
    template_name='watch/Sleep_create.html'

    def post(self,request, *args, **kwargs):
        super(SleepCreateView,self).post(request)
        messages.success(request, f"This Sleep Item Added")
        return redirect('sleep_list')

class SleepDeleteView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request,*args,**kwargs):
        sleep_pk=kwargs["pk"]
        delete_sleep=Sleep.objects.get(pk=sleep_pk)       
        messages.error(request, f"This Sleep Item Removed")
        delete_sleep.delete()
        
        return HttpResponseRedirect(reverse("sleep_list"))
