from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

def login_view(request):
    # Handle the login logic here
    return render(request, 'accounts/login.html')

def logout_view(request):
    # Handle the logout logic here
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

def register_view(request):
    # Handle the registration logic here
    return render(request, 'accounts/register.html')
