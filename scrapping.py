from bs4 import BeautifulSoup
import urllib.request as ur
from tkinter import Tk, Button, messagebox, Entry, Toplevel, Scrollbar, RIGHT, Y, Listbox, END, LEFT, BOTH, Label
import sqlite3
import re

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

def almacenar_salidas():
    print("################################ SALIDAS #################################")
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
                print(codigo_vuelo)
                aerolinea=c[1].get_text().strip()
                print(aerolinea)
                destino=c[2].get_text().strip()
                print(destino)
                hora_salida=c[3].get_text().strip()
                print(hora_salida)
                estado = c[4].get_text().strip()
                if estado.split()[-1] == 'Delayed':
                    estado = 'Con retraso'
                print(estado)
            print('=======================================')

def almacenar_llegadas():
    print("################################ LLEGADAS #################################")
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
                print(codigo_vuelo)
                aerolinea=c[1].get_text().strip()
                print(aerolinea)
                origen=c[2].get_text().strip()
                print(origen)
                hora_salida=c[3].get_text().strip()
                print(hora_salida)
                estado = c[4].get_text().strip()
                if estado.split()[-1] == 'Delayed':
                    estado = 'Con retraso'
                print(estado)
            print('=======================================')
            

if __name__ == "__main__":
    almacenar_salidas()
    almacenar_llegadas()