from django import forms
from django.contrib.auth.models import User
from coupark.models import UserProfileInfo
import re

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
    
    def clean_mail(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')

        return email

    def company_mail(self):

        email = self.cleaned_data.get('email')
        
        regex = r'\b[A-Za-z0-9._%+-]+@coupa.com'

        if (re.fullmatch(regex, email)):
            raise forms.ValidationError(u'Email addresses must belong to Coupa.')

        return email


class UserProfileInfoForm(forms.ModelForm):

    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic')
