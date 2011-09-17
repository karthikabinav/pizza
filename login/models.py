from django.db import models
from django.contrib.auth.models import User




"""
This model will store how much money was actually spent and 
how would have been spent
"""
class Money(models.Model):
	money_spent 	= models.IntegerField()
	money_saved	=	models.IntegerField()
	money_without_coupons	= models.IntegerField()

	def __unicode__(self):
		return self.money_saved
	
	class Admin:
		pass
	
"""
This model will store markers to user
Markers will initiate them to comeback and use it again
"""
class Marker(models.Model):
	C_initiate_marker	=	models.IntegerField()    	# Initiating the marker
	C_donar_marker	=	models.IntegerField()			#	Donating a marker
	C_use_marker	=	models.IntegerField()				# Using a marker
	C_R_initiate_marker	=	models.IntegerField()	# Leaving after initaiting a marker
	C_R_use_marker	=	models.IntegerField()			# Leaving after agring to buy stuff


	
class UserProfile(models.Model):
    user 			= models.ForeignKey		(User, unique = True)
    hostel = models.CharField(max_length=20)
    year =models.IntegerField()
    money = models.ForeignKey(Money)
    marker = models.ForeignKey(Marker)
    mobile_number = models.IntegerField()
        
    def __unicode__(self):
        return self.user.username

    class Admin:
        pass

"""
This model is used to store details about each of a 
particualr meet.
"""
class Details(models.Model):
	user	=	models.ForeignKey(UserProfile)
	money	=	models.ForeignKey(Money)
	
"""
This model is used to keep info about the pizza orders in a group
Each time a meet is done each users details are stored and with
amount of money spent by him
"""

class Meet(models.Model):
	CouponType		=	models.CharField(max_length =100)
	Initaiter	=	models.ForeignKey(Details)
	CouponUsers		=	models.ManyToManyField(Details,related_name="coupon users")
	Start_Time =models.DateTimeField()
	End_Time = models.DateTimeField(blank=True)
