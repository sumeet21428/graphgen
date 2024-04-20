from django.contrib import admin
from django.urls import path
from graphgen import views

urlpatterns = [
    path('', views.graph_view, name = 'home'),
    path('about', views.about, name = 'about'),
    path('services', views.services, name = 'services'),
    path('contacts', views.contacts, name = 'contacts'),
    
]