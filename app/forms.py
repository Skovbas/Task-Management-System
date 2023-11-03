from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from .models import Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text="Required. Add a valid email address.")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'required': '',
            'name': 'username',
            'id' : 'username',
            'type' : 'text',
            'class' : 'form-control form-control-lg',
            'maxlength' : '16',
            'minlength' : '6'
        })
        
        self.fields["email"].widget.attrs.update({
            'required': '',
            'name': 'email',
            'id' : 'email',
            'type' : 'email',
            'class' : 'form-control form-control-lg',
        })
        
        self.fields["password1"].widget.attrs.update({
            'required': '',
            'name': 'password1',
            'id' : 'password1',
            'type' : 'password',
            'class' : 'form-control form-control-lg',
            'maxlength' : '25',
            'minlength' : '8'
        })
        
        self.fields["password2"].widget.attrs.update({
            'required': '',
            'name': 'password2',
            'id' : 'password2',
            'type' : 'password',
            'class' : 'form-control form-control-lg',
            'maxlength' : '25',
            'minlength' : '8'
        })
        
    
    class Meta:
        model = Account
        fields = ('username', 'email', 'password1', 'password2')
        
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.get(email=email)
            raise forms.ValidationError(f'Email {email} is already in use.')
        except Account.DoesNotExist:
            return email

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.get(username=username)
            raise forms.ValidationError(f'Username {username} is already in use.')
        except Account.DoesNotExist:
            return username
    
            