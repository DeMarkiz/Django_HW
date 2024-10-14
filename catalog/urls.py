from django.contrib import admin
from django.urls import path
from . import views


app_name = 'catalog'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('contact/', views.contact, name='contact')
]