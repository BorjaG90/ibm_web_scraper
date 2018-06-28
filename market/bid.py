# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

from market.auction import *
from bs4 import BeautifulSoup

import requests

def make_bid(html_content, id_player, auth):
  session = requests.session()

  soup = BeautifulSoup(html_content, 'html.parser')
  final = soup.find("span",{"id":"claus"})
  if(final!=None): #I can bid
    puja = final.find(text=True, recursive=False)
    puja_max = soup.find("span",{"id":"clausmax"}).find(text=True, recursive=False)
    fich = soup.find("span",{"id":"fich"}).find(text=True, recursive=False)
    ano = soup.find("span",{"id":"ano"}).find(text=True, recursive=False)
    print("Puja: " + str(puja))
    print("PujaMax: " + str(puja_max))
    print("Ficha: " + str(fich))
    print("Años: " + str(ano))

    max_team = input("Introduzca Puja máxima para el Equipo: ")
    max_player = input("Introduzca Ficha máxima para el Jugador: ")
    years = input("Introduzca Años de Contrato: ")

    par = {
      "acc":"ofrecer",
      "tipo":"1",
      "id_jugador":str(id_player),
      "clausula":str(puja),
      "clausulamax":str(max_team),
      "ficha":str(max_player),
      "anos":str(years)
    }

    login(auth, session)

    url = "http://es.ibasketmanager.com/inicio.php?accion=/ofertapuja.php?acc=" + par['acc']
    url = url + "&tipo=" + par['tipo'] + "&id_jugador=" + par['id_jugador']
    url = url + "&clausula=" + par['clausula'] + "&clausulamax=" + par['clausulamax']
    url = url + "&ficha=" + par['ficha'] + "&anos=" + par['anos']
    # url = "http://es.ibasketmanager.com/inicio.php%3Faccion%3D/ofertapuja.php%3Facc%3D" + par['acc']
    # url = url + "%26tipo%3D" + par['tipo'] + "%26id_jugador%3D" + par['id_jugador']
    # url = url + "%26clausula%3D" + par['clausula'] + "%26clausulamax%3D" + par['clausulamax']
    # url = url + "%26ficha%3D" + par['ficha'] + "&anos%3D" + par['anos']
    print(url)
    r = session.get(url)
    load_status=0
    while load_status!=200:
        load_status = r.status_code
    print(BeautifulSoup(r.content, 'html.parser'))
    
    




def login(payload, session):
    
    login_url = 'http://es.ibasketmanager.com/loginweb.php'

    r = session.post(login_url, data = payload)

    load_status=0
    while load_status!=200:
        load_status = r.status_code
    print("\n[LogIn realizado con exito]\n")

