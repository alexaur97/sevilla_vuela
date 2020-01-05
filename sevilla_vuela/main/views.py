from django.shortcuts import render
from bs4 import BeautifulSoup
import urllib.request as ur
from .models import Salida, Llegada, Aerolinea
from django.http import HttpResponse

def inicio(request):
    Salida.objects.all().delete()
    Llegada.objects.all().delete()
    Aerolinea.objects.all().delete()
    scraping()
    return HttpResponse('<h1>Hecho</h1>')

def scraping():
    aerolineas=[]
    almacenar_llegadas(aerolineas)
    almacenar_salidas(aerolineas)

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

def almacenar_salidas(aerolineas):
    lista = salidas()
    for i in lista:
        vuelos = i.find_all('tr')
        for vuelo in vuelos:
            c = vuelo.find_all('td')
            a = c[0].find('a')
            if a != None:
                codigo_vuelo = a.get_text().strip()
                codigo_compartido = c[0].find('span')
                if codigo_compartido != None:
                    codigo_vuelo = codigo_vuelo + ' (codeshare)'
                
                aerolinea=c[1].get_text().strip()
                if aerolinea not in aerolineas:
                    aerolineas.append(aerolinea)
                    company = Aerolinea(nombre = aerolinea)
                    company.save()
                else:
                    company = Aerolinea.objects.get(nombre=aerolinea)
                
                destino=c[2].get_text().strip()
                hora_salida=c[3].get_text().strip()
                estado = c[4].get_text().strip()
                con_retraso = False
                if estado.split()[-1] == 'Delayed':
                    estado = 'Con retraso'
                    con_retraso=True
                
                salida = Salida(codigo_vuelo=codigo_vuelo, aerolinea=company, destino = destino, partida = hora_salida, estado = estado, con_retraso=con_retraso)
                salida.save()

def almacenar_llegadas(aerolineas):
    lista = llegadas()
    for i in lista:
        vuelos = i.find_all('tr')
        for vuelo in vuelos:
            c = vuelo.find_all('td')
            a = c[0].find('a')
            if a != None:
                codigo_vuelo = a.get_text().strip()
                codigo_compartido = c[0].find('span')
                if codigo_compartido != None:
                    codigo_vuelo = codigo_vuelo + ' (codeshare)'

                aerolinea=c[1].get_text().strip()
                if aerolinea not in aerolineas:
                    aerolineas.append(aerolinea)
                    company = Aerolinea(nombre = aerolinea)
                    company.save()
                else:
                    company = Aerolinea.objects.get(nombre=aerolinea)

                origen=c[2].get_text().strip()
                hora_llegada=c[3].get_text().strip()
                estado = c[4].get_text().strip()
                con_retraso=False
                if estado.split()[-1] == 'Delayed':
                    estado = estado + '(Con retraso)'
                    con_retraso=True
                
                llegada = Llegada(codigo_vuelo=codigo_vuelo, aerolinea=company, origen = origen, llegada = hora_llegada, estado = estado, con_retraso=con_retraso)
                llegada.save()