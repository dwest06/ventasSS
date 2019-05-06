from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, RegexValidator

class LoginForm(AuthenticationForm):

    class Meta:
        fields = ['username','password']
        labels = {
            'username' : 'Email',
            'password' : 'Clave'
        }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for campo in self.visible_fields():
            campo.field.widget.attrs['class'] = 'form-control'
            if campo.name == 'username':
                campo.field.widget.attrs['placeholder'] = 'E-mail'
            elif campo.name == 'password':
                campo.field.widget.attrs['placeholder'] = 'Clave'