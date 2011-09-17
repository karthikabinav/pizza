from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.models import User, Group
from django.template.loader import get_template
from django.template.context import Context, RequestContext
from django.utils.translation import ugettext as _
from django.core.mail import send_mail,EmailMessage,SMTPConnection
from django.contrib.sessions.models import Session
from django.utils import simplejson
from autometer.misc.util import * 
from autometer.settings import *
from autometer.login.models import *
from autometer.login import forms


import sha,random,datetime

def login (request):
       
    form=forms.LoginForm()
    if 'logged_in' in request.session and request.session['logged_in'] == True:
        return HttpResponseRedirect("%schangeFare/dashboard/" % settings.SITE_URL)
            
    if request.method == 'POST':
        data = request.POST.copy()
        form = forms.LoginForm(data)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data["password"])
            if user is not None:
                auth.login (request, user)
                try:
                    return HttpResponseRedirect("%schangeFare/dashboard/" % settings.SITE_URL)
                except:
                    return HttpResponseRedirect("%s" % settings.SITE_URL)        
            else:
                request.session['invalid_login'] = True
                request.session['logged_in'] = False
                errors=[]
                errors.append("Incorrect username and password combination!")
                return render_to_response('login.html', locals(),context_instance= global_context(request))
                 
        else:                       
            invalid_login = session_get(request, "invalid_login")
            form = forms.LoginForm () 
    return render_to_response('login.html', locals(), context_instance= global_context(request))

def register(request):
    
    #if request.user.is_authenticated():
        #logged_in = True
    
    
    if request.method=='POST':
        data = request.POST.copy()
        form = forms.AddUserForm(data)
        
        
        if form.is_valid():
            
            user = User.objects.create_user(username = form.cleaned_data['name'], email = form.cleaned_data['email'],password = form.cleaned_data['password'],)
            user.is_active= False
            user.save()
            
            

            user.name = form.cleaned_data['name']
            user.save()
            userprofile = UserProfile(
                    user = user,
                    mobile_number = form.cleaned_data['mobile_number'],
                    
                    )
            userprofile.save()
            request.session['registered_user'] = True

        return HttpResponseRedirect("%slogin/"%settings.SITE_URL)
    else:
        form = forms.AddUserForm()
        registered_user = session_get(request,'registered_user')
    return render_to_response('register.html', locals(), context_instance= global_context(request))    

def get_current_meets(request):

    cur_time=datetime.datetime.now()
    auto_meter_object = autometer.Meet.objets.all()
    
    cur_meets=[]
    
    for objects in auto_meter_object:
        if cur_time-objects.start_time > timedelta(seconds=5) and objects.end_time-cur_time < timedelta(seconds=5):
            cur_meets.append({"coupon_type":objects.CouponType,"initiater":objects.Initaiter,"CouponUsers": objects.CouponUsers.user.username,"start_time":objects.Start_Time,"end_time":objects.End_Time})
    
    
    return render_to_response('show_current_meets.html', locals(), context_instance= global_context(request))
     


    
    

