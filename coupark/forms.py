from django import forms
from django.contrib.auth.models import User
import re

# def company_mail(email):
 
#     regex = r'\b[A-Za-z0-9._%+-]+@coupa.com'

#     if (not re.fullmatch(regex, email)):
#         raise forms.ValidationError(u'Email addresses must belong to Coupa.')

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

