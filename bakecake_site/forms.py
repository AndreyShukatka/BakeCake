from django import forms
from django.contrib.auth import get_user_model
from .models import User


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'password'
        ]


class UserAuthorizationForm(forms.ModelForm):
    email = forms.EmailField(label='', widget=forms.EmailInput(
        attrs={'v-model':"EnteredNumber",
               'type': "text",
               'name': "email"}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'v-model':"EnteredNumber",
               'type': "text",
               'name': "password"}))
    type = forms.CharField(widget=forms.TextInput(attrs={'type': "hidden", 'value': 'login'}))

    class Meta:
        model = get_user_model()
        fields = ('email',)


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='', widget=forms.EmailInput())
    password = forms.CharField(label='', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ('email',)

