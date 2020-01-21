from django.shortcuts import render
from .models import Salida, Salida_comp, Llegada, Llegada_comp, Aerolinea
from .scrapping import scraping_aerolineas, scraping_vuelos
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.conf import settings
from .forms import vuelos_por_destino
from .forms import vuelos_por_origen
from django.template import loader




def inicio(request):
    if Aerolinea.objects.all().count() == 0:
        scraping_aerolineas()

    formulario1 = vuelos_por_destino()
    formulario2 = vuelos_por_origen()

    llegadas = None
    salidas = None
    destino = None
    origen = None

    post=0
    if request.method == 'POST':
        formulario1 = vuelos_por_destino(request.POST)
        formulario2 = vuelos_por_origen(request.POST)
        post=1
        
        
        if formulario1.is_valid():
            destino = formulario1.cleaned_data['destino']
            salidas = Salida.objects.filter(destino__contains=destino)
    
        
        if formulario2.is_valid():
            origen  = formulario2.cleaned_data['origen']
            llegadas = Llegada.objects.filter(origen__contains=origen)
    else:
        scraping_vuelos()

    return render(request, 'index.html', {'STATIC_URL':settings.STATIC_URL, 'post':post,'formulario1':formulario1, 'salidas':salidas, 'destino':destino, 'formulario2':formulario2, 'llegadas':llegadas, 'origen':origen})


def codigo_vuelos(request):
    all_llegadas_comp = Llegada_comp.objects.all()
    all_salidas_comp = Salida_comp.objects.all()
    template = loader.get_template('lista_codigo.html')
    context = {
        'all_llegadas_comp' : all_llegadas_comp, 'all_salidas_comp' : all_salidas_comp, 'STATIC_URL':settings.STATIC_URL,
    }
    result = template.render(context, request)
    return HttpResponse(result)


def listar_aerolineas(request):
    all_aerolineas = Aerolinea.objects.all()
    template = loader.get_template('aerolineas.html')
    context = {
        'all_aerolineas' : all_aerolineas, 'STATIC_URL':settings.STATIC_URL,
    }
    result = template.render(context, request)
    return HttpResponse(result)


def listar_vuelos(request):
    return render(request, 'vuelos.html', {'STATIC_URL':settings.STATIC_URL,})

def listar_llegadas(request):
    all_llegadas = Llegada.objects.all()
    template = loader.get_template('lista_llegadas.html')
    context = {
        'all_llegadas' : all_llegadas, 'STATIC_URL':settings.STATIC_URL,
    }
    result = template.render(context, request)
    return HttpResponse(result)

def listar_salidas(request):
    all_salidas = Salida.objects.all()
    template = loader.get_template('lista_salidas.html')
    context = {
        'all_salidas' : all_salidas, 'STATIC_URL':settings.STATIC_URL,
    }
    result = template.render(context, request)
    return HttpResponse(result)


def listar_llegadas_salidas(request, nombre_aerolinea):
    all_salidas = Salida_comp.objects.filter(aerolinea = nombre_aerolinea)
    all_llegadas = Llegada_comp.objects.filter(aerolinea = nombre_aerolinea)
    template = loader.get_template('lista_llegadas_salidas.html')
    context = {
        'all_salidas' : all_salidas, 'STATIC_URL':settings.STATIC_URL,
        'all_llegadas' : all_llegadas, 'STATIC_URL':settings.STATIC_URL,

    }
    result = template.render(context, request)
    return HttpResponse(result)

def about(request):
    return render(request, 'about.html')