"""sevilla_vuela URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio),
    path('inicio/', views.inicio),
    path('inicio.html/', views.inicio),
    path('about_us/', views.about),
    path('vuelos/', views.listar_vuelos),
    path('llegadas/', views.listar_llegadas),
    path('salidas/', views.listar_salidas),
    path('codeshare/', views.codigo_vuelos),
    path('aerolineas/', views.listar_aerolineas),
    path('aerolineas/<nombre_aerolinea>', views.listar_llegadas_salidas),
    path('refresh/', views.refrescar),

]
