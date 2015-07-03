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

