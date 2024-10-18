from django.contrib import admin
from django.urls import path
from django.urls import include
from accounts import views  # Import the views module
from django.http import HttpResponse
from django.contrib.auth.views import LoginView


# def home(request):
#     return HttpResponse("Welcome to the Social Book!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # your accounts URLs
    path('register/', views.register, name='register'),  # registration page
    path('', views.register, name='home'),  # set register as the home page
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
]
