# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
import django.contrib.auth.views
admin.autodiscover()

#handler404 = "main_test.misc.util.not_found"
#handler500 = "main_test.misc.util.server_error"


urlpatterns = patterns('',  
        
      
      (r'^login/?$', 'autometer.login.views.login'),
      (r'^logout/?$', 'autometers.login.views.logout'),
      

)   



