from django import forms
from Masters.models import *

class UserInfoForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = DimUserLogin
        widgets = {
        'password': forms.PasswordInput(),

    }
    	fields = '__all__'

class HosForm(forms.ModelForm):
    class Meta:
        model=HospitalDetails
        exclude = ['country','status']

class UserMaintenaceForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = UserMaintenance
        widgets = {
        'password': forms.PasswordInput(),

    }
    	fields='__all__'

