from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    # ('register/''register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('register/', views.register, name='register'),

]