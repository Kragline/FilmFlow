from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import CustomProfile


username_attrs = {'type': 'text', 'class': 'form-control', 'placeholder': 'Username'}
email_attrs = {'type': 'email', 'class': 'form-control', 'placeholder': 'name@example.com'}
password_attrs = {'type': 'password', 'class': 'form-control', 'placeholder': 'Password'}

first_name_attrs = {'type': 'text', 'class': 'form-control', 'placeholder': 'First name'}
last_name_attrs = {'type': 'text', 'class': 'form-control', 'placeholder': 'Last name'}

file_attrs = {'type': 'file', 'class': 'form-control'}


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs=username_attrs))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs=email_attrs))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs=password_attrs))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs=password_attrs))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs=username_attrs))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs=email_attrs))
    first_name = forms.CharField(label='First name', required=False, widget=forms.TextInput(attrs=first_name_attrs))
    last_name = forms.CharField(label='Last name', required=False, widget=forms.TextInput(attrs=last_name_attrs))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs=username_attrs))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs=password_attrs))


class CustomProfileForm(forms.ModelForm):
    class Meta:
        model = CustomProfile
        fields = ['profile_pic']

        widgets = {
            'profile_pic': forms.FileInput(attrs=file_attrs)
        }
