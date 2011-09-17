# -*- coding: utf-8 -*-
#We can use the same forms as last time for registation. We are not really changing anything here so.
#If we have to change anything it shouldn't be much of a problem
from django import forms
from django.forms import ModelForm
from django.db import models as d_models
import re 
from django.contrib.auth.models import User
from django.template import Template, Context
from django.utils.safestring import mark_safe

from autometer.login import models
from autometer import settings
 
alnum_re = re.compile(r'^[\w.-]+$') # regexp. from jamesodo in #django  [a-zA-Z0-9_.]
alphanumric = re.compile(r"[a-zA-Z0-9]+$")
            
class LoginForm(forms.Form):
    username=forms.CharField(help_text='Your Pizzomania username')
    password=forms.CharField(widget=forms.PasswordInput, help_text='Your password')
    

class AddUserForm(forms.Form):

    name      = forms.CharField  (max_length=30,
                                       help_text='Enter your first name here.')
    username       = forms.CharField  (max_length=30,
                                       help_text='30 characters or fewer. Letters, numbers and @/./+/-/_ characters')
    email          = forms.EmailField (help_text='Enter your e-mail address. eg, someone@gmail.com')
    password       = forms.CharField  (min_length=6,
                                       max_length=30,
                                       widget=forms.PasswordInput,
                                       help_text='Enter a password that you can remember')
    password_again = forms.CharField  (max_length=30,
                                       widget=forms.PasswordInput,
                                       help_text='Enter the same password that you entered above')
    
    mobile_number = forms.IntegerField()
    year=forms.IntegerField()
    class Meta:
        model = models.UserProfile
        fields=('name','username','password','password_again','email','mobile_number')
                
    
    def clean_username(self):
        if not alnum_re.search(self.cleaned_data['username']):
           raise forms.ValidationError(u'Usernames can only contain letters, numbers and underscores')
        if User.objects.filter(username=self.cleaned_data['username']):
            pass
        else:
            return self.cleaned_data['username']
        raise forms.ValidationError('This username is already taken. Please choose another.')

	    
    	  
    def clean_name(self):
	if not self.cleaned_data['name'].replace(' ','').isalpha():
	    raise forms.ValidationError(u'Names cannot contain anything other than alphabets.')
	else:
	    return self.cleaned_data['name']
	  
    
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']):
            pass
        else:
            return self.cleaned_data['email']
        raise forms.ValidationError('This email address is already taken. Please choose another.')

    def clean_password(self):
        if self.prefix:
            field_name1 = '%s-password'%self.prefix
            field_name2 = '%s-password_again'%self.prefix
        else:
            field_name1 = 'password'
            field_name2 = 'password_again'
            
        if self.data[field_name1] != '' and self.data[field_name1] != self.data[field_name2]:
            raise forms.ValidationError ("The entered passwords do not match.")
        else:
            return self.data[field_name1]
    

