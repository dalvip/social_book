from django.shortcuts import render
from django.shortcuts import render, redirect
from .views import *
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django import forms
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib import messages




class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

# def register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             login(request, user)
#             messages.success(request, "Registration successful!")
#             return redirect('/')
#     else:
#         form = RegisterForm()

#     return render(request, 'accounts/register.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Save the user object without committing immediately
            user = form.save(commit=False)
            # Set the user's password correctly using set_password
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Log in the user after registration
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('login')  # Redirect to the login page or home page
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

