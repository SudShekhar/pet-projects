from django import forms
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from wali.models import Discount

class OwnUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username','email', 'first_name', 'last_name']
	

class DiscountForm(forms.ModelForm):
	class Meta:
		model = Discount
		exclude = ["product_id","waiting_users","bought_by"]

