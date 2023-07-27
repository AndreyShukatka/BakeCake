from django import forms
from django.contrib.auth import get_user_model
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm


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


class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'v-model': "Name", 'type': "text", 'name': "name_format", 'id': "name", ':readonly':"!Edit", 'class': "form-control my-2 i cake__textinput"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'v-model': "Phone", 'type': "text", 'name': "phone_format", 'id':"phone", ':readonly':"!Edit", 'class': "form-control my-2 cake__textinput"}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'v-model': "Email", 'type': "text", 'name': "email_format", 'id':"email", ':readonly':"!Edit", 'class': "form-control my-2 cake__textinput"}))

    class Meta:
        model = User
        fields = (
            'username',
            'phone',
            'email'
        )
