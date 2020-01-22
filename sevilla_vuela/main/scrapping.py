from bs4 import BeautifulSoup
import urllib.request as ur
from .models import Salida, Salida_comp, Llegada, Llegada_comp, Aerolinea

def salidas():
    datos = ur.urlopen("https://www.flightstats.com/go/weblet?guid=34b64945a69b9cac:7b907964:13ed466ba45:3e7e&weblet=status&action=AirportFlightStatus&airportCode=SVQ")
    s = BeautifulSoup(datos, "lxml")
    lista = s.find_all("table", class_=["tableListingTable"])
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
                    operadora_url = c[0].find('a').get('href')
                    datos = ur.urlopen(operadora_url)
                    s = BeautifulSoup(datos, "lxml")
                    operadora = s.find("div", class_=["ticket__OperatedBy-s1rrbl5o-5","fbPHSm"]).get_text()
                    salida = Salida_comp(codigo_vuelo=codigo_vuelo, aerolinea=aerolinea, destino = destino, partida = hora_salida, estado = estado, con_retraso=con_retraso, operadora=operadora.replace('Operated by','Operado por'))
                else:
                    try:
                        company = Aerolinea.objects.get(nombre__endswith=aerolinea)
                    except:
                        try:
                            company = Aerolinea.objects.get(nombre__startswith=aerolinea)
                        except:
                            aer = Aerolinea(nombre = aerolinea, telefono = '', logo = '', email = '', url_web = '', es_habitual = False)
                            aer.save()
                            company = aer
                    salida = Salida(codigo_vuelo=codigo_vuelo, aerolinea=company, destino = destino, partida = hora_salida, estado = estado, con_retraso=con_retraso)
                salida.save()
                print('Almacenado con éxito',salida.codigo_vuelo)

def llegadas():
    datos = ur.urlopen("https://www.flightstats.com/go/weblet?guid=34b64945a69b9cac:7b907964:13ed466ba45:3e7e&weblet=status&action=AirportFlightStatus&airportCode=SVQ&airportQueryType=1")
    s = BeautifulSoup(datos, "lxml")
    lista = s.find_all("table", class_=["tableListingTable"])
    return lista

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
                    operadora_url = c[0].find('a').get('href')
                    datos = ur.urlopen(operadora_url)
                    s = BeautifulSoup(datos, "lxml")
                    operadora = s.find("div", class_=["ticket__OperatedBy-s1rrbl5o-5","fbPHSm"]).get_text()
                    llegada = Llegada_comp(codigo_vuelo=codigo_vuelo, aerolinea=aerolinea, origen = origen, hora_llegada=hora_llegada, estado = estado, con_retraso=con_retraso, operadora=operadora.replace('Operated by','Operado por'))
                else:
                    try:
                        company = Aerolinea.objects.get(nombre__endswith=aerolinea)
                    except:
                        try:
                            company = Aerolinea.objects.get(nombre__startswith=aerolinea)
                        except:
                            aer = Aerolinea(nombre = aerolinea, telefono = '', logo = '', email = '', url_web = '', es_habitual = False)
                            aer.save()
                            company = aer
                    llegada = Llegada(codigo_vuelo=codigo_vuelo, aerolinea=company, origen = origen, hora_llegada=hora_llegada, estado = estado, con_retraso=con_retraso)
                llegada.save()
                print('Almacenado con éxito',llegada.codigo_vuelo)

def aerolineas(): 
    datos = ur.urlopen("http://www.aena.es/es/aeropuerto-sevilla/companias-aereas.html")
    s = BeautifulSoup(datos, "lxml")
    lista = s.find("tbody")   
    return lista

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
        url_logo = divs.find("img").get("src")
        companyInfo= divs.find("div", class_=["companyInfo"])
        
        datos_ficha = companyInfo.find("ul", class_= ["datos_ficha"])
        datos = datos_ficha.find_all("li")
        correo=None
        web= None
        for d in datos:
            da = d.get_text()
            if "Web" in da :
                startLoc = 5
                endLoc = len(da)
                web = da[startLoc: endLoc]
            if "Correo electrónico" in da:
                startLoc = 20
                endLoc = len(da)
                correo = da[startLoc: endLoc]

        aerolinea = Aerolinea(nombre = nombre, telefono = telefono, logo = 'http://www.aena.es'+url_logo, email = correo, url_web = web, es_habitual = True)
        aerolinea.save()
        print('Almacenada con éxito',aerolinea.nombre)

def scraping_aerolineas():
    Aerolinea.objects.all().delete()
    print('Almacenando aerolíneas...................')
    almacenar_aerolineas()
    print(Aerolinea.objects.all().count(),'Aerolíneas almacenadas con éxito...................')

def scraping_vuelos():
    Salida.objects.all().delete()
    Llegada.objects.all().delete()
    Salida_comp.objects.all().delete()
    Llegada_comp.objects.all().delete()
    print('Almacenando vuelos...................')
    almacenar_llegadas()
    almacenar_salidas()
    print('Vuelos almacenados con éxito...................')

