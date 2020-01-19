from django.shortcuts import render
from bs4 import BeautifulSoup
import urllib.request as ur
from .models import Salida, Salida_comp, Llegada, Llegada_comp, Aerolinea
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.conf import settings
from .forms import vuelos_por_destino
from .forms import vuelos_por_origen
from django.template import loader


def inicio(request):
    try:
        #Aerolinea.objects.all().delete()        
        #Salida.objects.all().delete()
        #Llegada.objects.all().delete()
        scraping_vuelos()
    except ObjectDoesNotExist:
        scraping_aerolineas()



    formulario1 = vuelos_por_destino()
    formulario2 = vuelos_por_origen()

    llegadas = None
    salidas = None
    destino=None

    post=0
    if request.method == 'POST':
        formulario1 = vuelos_por_destino(request.POST)
        post=1
        
        if formulario1.is_valid():
            destino = formulario1.cleaned_data['destino']
            salidas = Salida.objects.filter(destino__contains=destino)


    if request.method == 'POST':
        formulario2 = vuelos_por_origen(request.POST)
        post=1
        
        if formulario2.is_valid():
            llegadas = Llegada.objects.filter(origen__contains=formulario2.cleaned_data['origen'])

    return render(request, 'index.html', {'STATIC_URL':settings.STATIC_URL, 'post':post,'formulario1':formulario1, 'salidas':salidas, 'destino':destino})


def scraping_aerolineas():
    return None

def scraping_vuelos():
    almacenar_aerolineas()
    almacenar_llegadas()
    almacenar_salidas()
   


def salidas():
    datos = ur.urlopen("https://www.flightstats.com/go/weblet?guid=34b64945a69b9cac:7b907964:13ed466ba45:3e7e&weblet=status&action=AirportFlightStatus&airportCode=SVQ")
    s = BeautifulSoup(datos, "lxml")
    lista = s.find_all("table", class_=["tableListingTable"])
    return lista

def llegadas():
    datos = ur.urlopen("https://www.flightstats.com/go/weblet?guid=34b64945a69b9cac:7b907964:13ed466ba45:3e7e&weblet=status&action=AirportFlightStatus&airportCode=SVQ&airportQueryType=1")
    s = BeautifulSoup(datos, "lxml")
    lista = s.find_all("table", class_=["tableListingTable"])
    return lista

def aerolineas(): 
    datos = ur.urlopen("http://www.aena.es/es/aeropuerto-sevilla/companias-aereas.html")
    s = BeautifulSoup(datos, "lxml")
    lista = s.find("tbody")   
    return lista

def almacenar_salidas():
    lista = salidas()
    for i in lista:
        vuelos = i.find_all('tr')
        for vuelo in vuelos:
            c = vuelo.find_all('td')
            a = c[0].find('a')
            if a != None:
                codigo_vuelo = a.get_text().strip()
                aerolinea=c[1].get_text().strip()
                destino=c[2].get_text().strip()
                hora_salida=c[3].get_text().strip()
                estado = c[4].get_text().strip()
                con_retraso = False
                
                if estado.split()[-1] == 'Delayed':
                    con_retraso=True
                
                codigo_compartido = c[0].find('span')
                if codigo_compartido != None:
                    codigo_vuelo = codigo_vuelo + ' (codeshare)'
                    operadora_url = c[0].find('a').get('href')
                    datos = ur.urlopen(operadora_url)
                    s = BeautifulSoup(datos, "lxml")
                    operadora = s.find("div", class_=["ticket__OperatedBy-s1rrbl5o-5","fbPHSm"]).get_text()
                    salida = Salida_comp(codigo_vuelo=codigo_vuelo, aerolinea=aerolinea, destino = destino, partida = hora_salida, estado = estado, con_retraso=con_retraso, operadora=operadora)
                else:
                    company = Aerolinea.objects.get(nombre=aerolinea)
                    salida = Salida(codigo_vuelo=codigo_vuelo, aerolinea=company, destino = destino, partida = hora_salida, estado = estado, con_retraso=con_retraso)
                salida.save()

def almacenar_llegadas():
    lista = llegadas()
    for i in lista:
        vuelos = i.find_all('tr')
        for vuelo in vuelos:
            c = vuelo.find_all('td')
            a = c[0].find('a')
            if a != None:
                codigo_vuelo = a.get_text().strip()
                aerolinea=c[1].get_text().strip()
                origen=c[2].get_text().strip()
                hora_llegada=c[3].get_text().strip()
                estado = c[4].get_text().strip()
                con_retraso=False
                
                if estado.split()[-1] == 'Delayed':
                    con_retraso=True
                
                codigo_compartido = c[0].find('span')
                if codigo_compartido != None:
                    codigo_vuelo = codigo_vuelo + ' (codeshare)'
                    operadora_url = c[0].find('a').get('href')
                    datos = ur.urlopen(operadora_url)
                    s = BeautifulSoup(datos, "lxml")
                    operadora = s.find("div", class_=["ticket__OperatedBy-s1rrbl5o-5","fbPHSm"]).get_text()
                    llegada = Llegada_comp(codigo_vuelo=codigo_vuelo, aerolinea=aerolinea, origen = origen, llegada = hora_llegada, estado = estado, con_retraso=con_retraso, operadora=operadora)
                else:
                    company = Aerolinea.objects.get(nombre=aerolinea)
                    llegada = Llegada(codigo_vuelo=codigo_vuelo, aerolinea=company, origen = origen, llegada = hora_llegada, estado = estado, con_retraso=con_retraso)
                llegada.save()


def almacenar_aerolineas():
    lista = aerolineas()
    trs = lista.find_all('tr', class_="")
    for t in trs:
        nombre = t.find('a').get_text()
        telefono = t.find('td').next_sibling.get_text()
        url = t.find('a').get('href')
        datos = ur.urlopen("http://www.aena.es" + url)
        s = BeautifulSoup(datos, "lxml")
        divs = s.find("div", class_=["datos_interes"])
      
    

               

def about(request):
    return render(request, 'about.html')


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
