from django import forms
from django.contrib.auth.models import User
from coupark.models import UserProfileInfo
import re

def company_mail(email):
 
    regex = r'\b[A-Za-z0-9._%+-]+@coupa.com'

    if (not re.fullmatch(regex, email)):
        raise forms.ValidationError(u'Email addresses must belong to Coupa.')

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(validators=[company_mail])

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class UserProfileInfoForm(forms.ModelForm):

    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)
