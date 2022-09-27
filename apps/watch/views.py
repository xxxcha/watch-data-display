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
import time
from .models import Watch, PPG, ECG, ACC, GYR
from .forms import WatchCreateForm,PPGCreateForm,ECGCreateForm,ACCCreateForm,GYRCreateForm


PAGINATOR_NUMBER = 10

class HomeView(LoginRequiredMixin,TemplateView):
    login_url = 'login'
    template_name = "index.html"
    context={}

    def get(self,request, *args, **kwargs):

        watch_count = Watch.objects.all().count()
        
        data_count = {"ppg":PPG.objects.all().count(),
                    "ecg":ECG.objects.all().count(),
                    "acc":ACC.objects.all().count(),
                    "gyr":GYR.objects.all().count()}
        all_count=data_count['ppg']+data_count['ecg']+data_count['acc']+data_count['gyr']       
        
        current_week = date.today().isocalendar()[1]
        
        self.context['watch_count']=watch_count
        self.context['data_count']=data_count
        self.context['all_count']=all_count

        return render(request, self.template_name, self.context)

class WatchListView(LoginRequiredMixin,ListView):
    login_url = 'login'
    model=Watch
    context_object_name = 'watch_list'
    template_name = 'watch/watch_list.html'
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
    template_name='watch/watch_create.html'

    def post(self,request, *args, **kwargs):
        super(WatchCreateView,self).post(request)
        new_watch_name = request.POST['name']
        return redirect('watch_list')

class WatchDeleteView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request,*args,**kwargs):
        watch_pk=kwargs["pk"]
        delete_watch=Watch.objects.get(pk=watch_pk)
        #model_name = delete_watch.__class__.__name__
        delete_watch.delete()
        
        return HttpResponseRedirect(reverse("watch_list"))

class PPGChartView(LoginRequiredMixin,TemplateView):
    template_name = "watch/ppg_chart.html"
    login_url = 'login'
    context={}
    all_watches = Watch.objects.values()
    watch_list = [x['name'] for x in all_watches]

    def get(self, request, *args, **kwargs):        
        watch_name = self.request.GET.get("watch_name")
        ppg_index =self.request.GET.get("ppg_index") 

        if not watch_name:
            watch_name=Watch.objects.values('name')[0]['name']
        
        index_list=[x['index'] for x in PPG.objects.filter(watch__name__exact=watch_name).values('index').distinct()]

        if not ppg_index:
            ppg_index=index_list[-1]

        ppg_data = PPG.objects.filter(
            Q(index=ppg_index)&Q(watch__name__exact=watch_name)
        )
         
        ppg_time = PPG.objects.filter(index=ppg_index).order_by('created').values('created')[0]['created']
        ppg_time = time.mktime(ppg_time.timetuple())*1000
        
        ppg_freq = PPG.objects.filter(index=ppg_index).values('freq')[0]['freq']

        data={
            'green': [[i/ppg_freq, ppg_data.values('green')[i]['green']] for i in range(len(ppg_data))],
            'red': [[i/ppg_freq, ppg_data.values('red')[i]['red']] for i in range(len(ppg_data))],
            'ir': [[i/ppg_freq, ppg_data.values('ir')[i]['ir']] for i in range(len(ppg_data))],        
        }

        self.context['watch_list']=self.watch_list
        self.context['index_list']=index_list
        self.context['watch_name']=watch_name
        self.context['ppg_index']=ppg_index
        self.context['ppg_time']=ppg_time
        self.context['ppg_freq']=ppg_freq
        self.context['data']=data

        return render(request, self.template_name, self.context)


class PPGListView(ListView):
    model=PPG
    context_object_name = 'ppg_list'
    template_name = 'watch/ppg_list.html'
    all_watches = Watch.objects.values()
    watch_list = [x['name'] for x in all_watches]
    watch_name=''
    ppg_index=''
    index_list=[]

    def get_queryset(self):
        watch_name = self.request.GET.get("watch_name")
        ppg_index =self.request.GET.get("ppg_index") 

        if watch_name:
            all_ppg = PPG.objects.all().filter(watch__name__exact=watch_name)
            self.watch_name=watch_name
            self.index_list=[x['index'] for x in PPG.objects.filter(watch__name__exact=watch_name).values('index').distinct()]

        else:
            all_ppg = PPG.objects.all().order_by("-id")

        if ppg_index:
            all_ppg = all_ppg.filter(index=ppg_index).order_by("-id")
            self.ppg_index=ppg_index
        else:
            all_ppg = all_ppg.order_by("-id")

        self.count_total = all_ppg.count()
        paginator = Paginator(all_ppg, PAGINATOR_NUMBER)
        page = self.request.GET.get('page')
        ppg = paginator.get_page(page)

        return ppg

    def get_context_data(self, *args, **kwargs):
        context = super(PPGListView, self).get_context_data(*args, **kwargs)
        context['watch_list'] = self.watch_list
        context['index_list'] = self.index_list
        context['watch_name'] = self.watch_name
        context['ppg_index'] = self.ppg_index
        context['count_total'] = self.count_total
        context['page_objects'] = self.get_queryset()
        return context

class PPGCreateView(LoginRequiredMixin,CreateView):
    model=PPG
    login_url = 'login'
    form_class=PPGCreateForm    
    template_name='watch/ppg_create.html'

    def post(self,request, *args, **kwargs):
        super(PPGCreateView,self).post(request)
        return redirect('ppg_list')

class PPGDeleteView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request,*args,**kwargs):
        ppg_pk=kwargs["pk"]
        delete_ppg=PPG.objects.get(pk=ppg_pk)       
        delete_ppg.delete()
        
        return HttpResponseRedirect(reverse("ppg_list"))

class ECGChartView(LoginRequiredMixin,TemplateView):
    template_name = "watch/ecg_chart.html"
    login_url = 'login'
    context={}
    all_watches = Watch.objects.values()
    watch_list = [x['name'] for x in all_watches]

    def get(self, request, *args, **kwargs):        
        watch_name = self.request.GET.get("watch_name")
        ecg_index =self.request.GET.get("ecg_index") 

        if not watch_name:
            watch_name=Watch.objects.values('name')[0]['name']
        
        index_list=[x['index'] for x in ECG.objects.filter(watch__name__exact=watch_name).values('index').distinct()]

        if not ecg_index:
            ecg_index=index_list[-1]

        ecg_data = ECG.objects.filter(
            Q(index=ecg_index)&Q(watch__name__exact=watch_name)
        )
         
        ecg_time = ECG.objects.filter(index=ecg_index).order_by('created').values('created')[0]['created']
        ecg_time = time.mktime(ecg_time.timetuple())*1000
        
        ecg_freq = ECG.objects.filter(index=ecg_index).values('freq')[0]['freq']

        data={
            'mv': [[i/ecg_freq, ecg_data.values('mv')[i]['mv']] for i in range(len(ecg_data))],      
        }

        self.context['watch_list']=self.watch_list
        self.context['index_list']=index_list
        self.context['watch_name']=watch_name
        self.context['ecg_index']=ecg_index
        self.context['ecg_time']=ecg_time
        self.context['ecg_freq']=ecg_freq
        self.context['data']=data

        return render(request, self.template_name, self.context)


class ECGListView(ListView):
    model=ECG
    context_object_name = 'ecg_list'
    template_name = 'watch/ecg_list.html'
    all_watches = Watch.objects.values()
    watch_list = [x['name'] for x in all_watches]
    watch_name=''
    ecg_index=''
    index_list=[]

    def get_queryset(self):
        watch_name = self.request.GET.get("watch_name")
        ecg_index =self.request.GET.get("ecg_index") 

        if watch_name:
            all_ecg = ECG.objects.all().filter(watch__name__exact=watch_name)
            self.watch_name=watch_name
            self.index_list=[x['index'] for x in ECG.objects.filter(watch__name__exact=watch_name).values('index').distinct()]

        else:
            all_ecg = ECG.objects.all().order_by("-id")

        if ecg_index:
            all_ecg = all_ecg.filter(index=ecg_index).order_by("-id")
            self.ecg_index=ecg_index
        else:
            all_ecg = all_ecg.order_by("-id")

        self.count_total = all_ecg.count()
        paginator = Paginator(all_ecg, PAGINATOR_NUMBER)
        page = self.request.GET.get('page')
        ecg = paginator.get_page(page)

        return ecg

    def get_context_data(self, *args, **kwargs):
        context = super(ECGListView, self).get_context_data(*args, **kwargs)
        context['watch_list'] = self.watch_list
        context['index_list'] = self.index_list
        context['watch_name'] = self.watch_name
        context['ecg_index'] = self.ecg_index
        context['count_total'] = self.count_total
        context['page_objects'] = self.get_queryset()
        return context

class ECGCreateView(LoginRequiredMixin,CreateView):
    model=ECG
    login_url = 'login'
    form_class=ECGCreateForm    
    template_name='watch/ecg_create.html'

    def post(self,request, *args, **kwargs):
        super(ECGCreateView,self).post(request)
        return redirect('ecg_list')

class ECGDeleteView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request,*args,**kwargs):
        ecg_pk=kwargs["pk"]
        delete_ecg=ECG.objects.get(pk=ecg_pk)       
        delete_ecg.delete()
        
        return HttpResponseRedirect(reverse("ecg_list"))

class ACCChartView(LoginRequiredMixin,TemplateView):
    template_name = "watch/acc_chart.html"
    login_url = 'login'
    context={}
    all_watches = Watch.objects.values()
    watch_list = [x['name'] for x in all_watches]

    def get(self, request, *args, **kwargs):        
        watch_name = self.request.GET.get("watch_name")
        acc_index =self.request.GET.get("acc_index") 

        if not watch_name:
            watch_name=Watch.objects.values('name')[0]['name']
        
        index_list=[x['index'] for x in ACC.objects.filter(watch__name__exact=watch_name).values('index').distinct()]

        if not acc_index:
            acc_index=index_list[-1]

        acc_data = ACC.objects.filter(
            Q(index=acc_index)&Q(watch__name__exact=watch_name)
        )
         
        acc_time = ACC.objects.filter(index=acc_index).order_by('created').values('created')[0]['created']
        acc_time = time.mktime(acc_time.timetuple())*1000
        
        acc_freq = ACC.objects.filter(index=acc_index).values('freq')[0]['freq']

        data={
            'x': [[i/acc_freq, acc_data.values('x')[i]['x']] for i in range(len(acc_data))],
            'y': [[i/acc_freq, acc_data.values('y')[i]['y']] for i in range(len(acc_data))],
            'z': [[i/acc_freq, acc_data.values('z')[i]['z']] for i in range(len(acc_data))]
        }

        self.context['watch_list']=self.watch_list
        self.context['index_list']=index_list
        self.context['watch_name']=watch_name
        self.context['acc_index']=acc_index
        self.context['acc_time']=acc_time
        self.context['acc_freq']=acc_freq
        self.context['data']=data

        return render(request, self.template_name, self.context)

class ACCListView(ListView):
    model=ACC
    context_object_name = 'acc_list'
    template_name = 'watch/acc_list.html'
    all_watches = Watch.objects.values()
    watch_list = [x['name'] for x in all_watches]
    watch_name=''
    acc_index=''
    index_list=[]

    def get_queryset(self):
        watch_name = self.request.GET.get("watch_name")
        acc_index =self.request.GET.get("acc_index") 

        if watch_name:
            all_acc = ACC.objects.all().filter(watch__name__exact=watch_name)
            self.watch_name=watch_name
            self.index_list=[x['index'] for x in ACC.objects.filter(watch__name__exact=watch_name).values('index').distinct()]

        else:
            all_acc = ACC.objects.all().order_by("-id")

        if acc_index:
            all_acc = all_acc.filter(index=acc_index).order_by("-id")
            self.acc_index=acc_index
        else:
            all_acc = all_acc.order_by("-id")

        self.count_total = all_acc.count()
        paginator = Paginator(all_acc, PAGINATOR_NUMBER)
        page = self.request.GET.get('page')
        acc = paginator.get_page(page)

        return acc

    def get_context_data(self, *args, **kwargs):
        context = super(ACCListView, self).get_context_data(*args, **kwargs)
        context['watch_list'] = self.watch_list
        context['index_list'] = self.index_list
        context['watch_name'] = self.watch_name
        context['acc_index'] = self.acc_index
        context['count_total'] = self.count_total
        context['page_objects'] = self.get_queryset()
        return context

class ACCCreateView(LoginRequiredMixin,CreateView):
    model=ACC
    login_url = 'login'
    form_class=ACCCreateForm    
    template_name='watch/acc_create.html'

    def post(self,request, *args, **kwargs):
        super(ACCCreateView,self).post(request)
        return redirect('acc_list')

class ACCDeleteView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request,*args,**kwargs):
        acc_pk=kwargs["pk"]
        delete_acc=ACC.objects.get(pk=acc_pk)       
        delete_acc.delete()
        
        return HttpResponseRedirect(reverse("acc_list"))

class GYRChartView(LoginRequiredMixin,TemplateView):
    template_name = "watch/gyr_chart.html"
    login_url = 'login'
    context={}
    all_watches = Watch.objects.values()
    watch_list = [x['name'] for x in all_watches]

    def get(self, request, *args, **kwargs):        
        watch_name = self.request.GET.get("watch_name")
        gyr_index =self.request.GET.get("gyr_index") 

        if not watch_name:
            watch_name=Watch.objects.values('name')[0]['name']
        
        index_list=[x['index'] for x in GYR.objects.filter(watch__name__exact=watch_name).values('index').distinct()]

        if not gyr_index:
            gyr_index=index_list[-1]

        gyr_data = GYR.objects.filter(
            Q(index=gyr_index)&Q(watch__name__exact=watch_name)
        )
         
        gyr_time = GYR.objects.filter(index=gyr_index).order_by('created').values('created')[0]['created']
        gyr_time = time.mktime(gyr_time.timetuple())*1000
        
        gyr_freq = GYR.objects.filter(index=gyr_index).values('freq')[0]['freq']

        data={
            'x': [[i/gyr_freq, gyr_data.values('x')[i]['x']] for i in range(len(gyr_data))],
            'y': [[i/gyr_freq, gyr_data.values('y')[i]['y']] for i in range(len(gyr_data))],
            'z': [[i/gyr_freq, gyr_data.values('z')[i]['z']] for i in range(len(gyr_data))]
        }
        print(gyr_time,gyr_freq,data)
        self.context['watch_list']=self.watch_list
        self.context['index_list']=index_list
        self.context['watch_name']=watch_name
        self.context['gyr_index']=gyr_index
        self.context['gyr_time']=gyr_time
        self.context['gyr_freq']=gyr_freq
        self.context['data']=data

        return render(request, self.template_name, self.context)

class GYRListView(ListView):
    model=GYR
    context_object_name = 'gyr_list'
    template_name = 'watch/gyr_list.html'
    all_watches = Watch.objects.values()
    watch_list = [x['name'] for x in all_watches]
    watch_name=''
    gyr_index=''
    index_list=[]

    def get_queryset(self):
        watch_name = self.request.GET.get("watch_name")
        gyr_index =self.request.GET.get("gyr_index") 

        if watch_name:
            all_gyr = GYR.objects.all().filter(watch__name__exact=watch_name)
            self.watch_name=watch_name
            self.index_list=[x['index'] for x in GYR.objects.filter(watch__name__exact=watch_name).values('index').distinct()]

        else:
            all_gyr = GYR.objects.all().order_by("-id")

        if gyr_index:
            all_gyr = all_gyr.filter(index=gyr_index).order_by("-id")
            self.gyr_index=gyr_index
        else:
            all_gyr = all_gyr.order_by("-id")

        self.count_total = all_gyr.count()
        paginator = Paginator(all_gyr, PAGINATOR_NUMBER)
        page = self.request.GET.get('page')
        gyr = paginator.get_page(page)

        return gyr

    def get_context_data(self, *args, **kwargs):
        context = super(GYRListView, self).get_context_data(*args, **kwargs)
        context['watch_list'] = self.watch_list
        context['index_list'] = self.index_list
        context['watch_name'] = self.watch_name
        context['gyr_index'] = self.gyr_index
        context['count_total'] = self.count_total
        context['page_objects'] = self.get_queryset()
        return context

class GYRCreateView(LoginRequiredMixin,CreateView):
    model=GYR
    login_url = 'login'
    form_class=GYRCreateForm    
    template_name='watch/gyr_create.html'

    def post(self,request, *args, **kwargs):
        super(GYRCreateView,self).post(request)
        return redirect('gyr_list')

class GYRDeleteView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request,*args,**kwargs):
        gyr_pk=kwargs["pk"]
        delete_gyr=GYR.objects.get(pk=gyr_pk)       
        delete_gyr.delete()
        
        return HttpResponseRedirect(reverse("gyr_list"))



