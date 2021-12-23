from django import forms
from .models import Order
from django.forms import PasswordInput
from django.views.generic import View
from django.contrib.auth.models import User
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View, DetailView
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType

class LoginForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'text', 'id': 'inputText', 'placeholder': ' Username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'type': 'password', 'id': 'inputPassword', 'placeholder': ' Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Username"
        self.fields['password'].label = "Password"

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'There in no such user in system')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Password is incorrect')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']



class RegistrationForm(forms.ModelForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'id': 'inputText', 'placeholder': ' Username'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'type': 'password', 'id': 'inputConfirmationPassword', 'placeholder': ' Confirm Password'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'type': 'password', 'id': 'inputPassword', 'placeholder': ' Password'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'type': 'email', 'id': 'inputEmail', 'placeholder': ' Email', 'class': 'text'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'text', 'id': 'inputText', 'placeholder': ' First Name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'type': 'text', 'id': 'inputText', 'placeholder': ' Last Name'}))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['first_name'].label = ''
        self.fields['last_name'].label = ''
        self.fields['email'].label = ''
        self.fields['password'].label = ''
        self.fields['confirm_password'].label = ''

    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('.')[-1]
        if domain in ['net']:
            raise forms.ValidationError(f'Validation cannot be aplied')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'This adress already exist')
        return email

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Passwords are not similar')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password'] #'confirm_password'

class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата получения заказа'

        order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_date', 'comment'
        )
