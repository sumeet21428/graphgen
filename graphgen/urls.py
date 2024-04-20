"""
URL configuration for graphgen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.contrib import admin
from django.urls import path, include
from graphgen_app import views

admin.site.site_header = "Niti Aayog Internship Project"
admin.site.site_title = "NITI Aayog internship Project"
admin.site.index_title = "Welcome!!"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.graph_view, name='graph'),
    #path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('', views.graph_view, name='graph'),
    path('services/', views.services, name='services'),
    path('wpi/', views.wpi, name='wpi'),
    path('cpi/', views.cpi, name='cpi'),
    path('exchange-rate/', views.exchange, name='exchange-rate'),
    path('foreign-reserves/', views.foreignreserves, name='foreign-reserves'),
    path('key-rates/', views.keyrates, name='key-rates'),
    path('gdp/', views.gdp, name='gdp'),
    path('scb-food-bank/', views.scbfoodbank, name='scb-food-bank'),
    path('balance-of-payments/', views.balanceofpayments, name='balance-of-payments'),
    path('search_results/', views.search_results, name='search_results'),
    path('iip/', views.iip, name='IIP'),
    path('documentation/', views.documentation, name='documentation'),
    path('fdi/', views.fdi, name='fdi'),
    path('gcpi/', views.gcpi, name='gcpi'),
    path('gfdi/', views.gfdi, name='gfdi'),
    path('ggdp/', views.ggdp, name='ggdp'),
    path('GForex/', views.GForex, name='GForex'),
    path('ggni/', views.ggni, name='ggni'),
    path('GEmissions/', views.GEmissions, name='GEmissions'),
    path('GForest/', views.GForest, name='GForest'),
    path('GRenewables/', views.GRenewables, name='GRenewables'),
    #path('/graph', views.graph_view, name='graph'),
    # path('', include('graphgen_app.urls'))
]

# Path: graphgen/graphgen_app/views.py