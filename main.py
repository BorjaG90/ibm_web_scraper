# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

import os
import getpass
import requests

from pymongo import MongoClient
from enum import Enum
from requests.auth import HTTPBasicAuth
from lxml import html

from transfers.readWebPage import *
from market.readWebPage import *
from statistics.readWebPage import *
from roster.readWebPage import *

#--Variables--
class AVERAGE(Enum):
    ALL = -1
    _0_20 = 0
    _21_25 = 1
    _26_30 = 2
    _31_35 = 3
    _36_40 = 4
    _41_45 = 5
    _46_50 = 6
    _51_55 = 7
    _56_60 = 8
    _61_65 = 9
    _66_70 = 10
    _71_75 = 11
    _76_80 = 12
    _81_85 = 13
    _86_90 = 14
    _91_95 = 15
    _96_99 = 16

class POSITION(Enum):
    ALL = -1
    BASE = 1
    ESCOLTA = 2
    ALERO = 3
    ALAPIVOT = 4
    PIVOT = 5

class TIME(Enum):
    _2H = 0
    _4H = 1
    _24H = 2
    _24_48H = 3
    _48_72H = 4

url = 'http://es.ibasketmanager.com/'

def login(payload):
    
    login_url = url + 'loginweb.php'

    r = session.post(login_url, data = payload)

    load_status=0
    while load_status!=200:
        load_status = r.status_code
    print("\n[LogIn realizado con exito]\n")

def analyze_player_similars(id_player, log, auth):
    """Option of web scrap similar buys of a player"""
    #Login
    if log:
        login(auth)

    transactions_url = url + 'jugador_compras_similares.php?id_jugador=' + str(id_player)
    
    r = session.get(transactions_url)
    load_status=0
    while load_status!=200:
        load_status = r.status_code
    # print("\n###[Similares Cargado]###")
    
    ts = analyze_similar_buys(r.content)
    for t in ts:
        #print("\t{}".format(t))
        if(db.transactions.find({"_id_player":t._id_player}, {"_id_date_buy":t._id_date_buy}).count() == 0):
            db.transactions.insert_one(t.to_db_collection())
        else:
             #print("\t-Ya existe-")
            db.transactions.replace_one({"$and":[{"_id_player":t._id_player}, 
                {"_id_date_buy":t._id_date_buy}]},t.to_db_collection())

def analyze_market_web(params):
    #print(params)
    market_url = url +'mercado.php?juvenil=' + str(params["juvenil"])
    market_url = market_url + "&tiempos=" + str(params["tiempos"])
    market_url = market_url + "&posiciones=" + str(params["posiciones"])
    market_url = market_url + "&calidad=" + str(params["calidad"]) 
    market_url = market_url + '&edad' + str(params["edad"])
    market_url = market_url + "&cdirecta=" + str(params["cdirecta"])
    
    #Access to pag
    print(' >{ ' + market_url + ' }')
    r = session.get(market_url)
    load_status=0
    while load_status!=200:
        load_status = r.status_code
    #print("\n#[Mercado Cargado]#")
    aus = analyze_market(r.content)
     
    #Insert into DB
    for a in aus:
        #print("\t{}".format(a))
        db.market.insert_one(a.to_db_collection())
    
    #Analyze similars
    for a in aus:
        analyze_player_similars(a._id, False, None)

def analyze_teams_web(division, group):
    standings_url = url + 'liga.php?temporada=' + str(season) + '&division=' + str(division) + '&grupo=' + str(group)
    print(' >{ ' + standings_url + ' }')
    r = session.get(standings_url)
    load_status=0
    while load_status!=200:
        load_status = r.status_code
    #print("\n#[Clasificacion Cargado]#")
    
    #Obtain teams of the standing
    teams_url = analyze_standings(r.content)

    for team_url in teams_url:
        juniors_url = url + 'plantilla.php?id_equipo=' + team_url + '&juveniles=1'
        print('  - Equipo ' + team_url +' :[ ' + juniors_url + ' ]')
        
        r = session.get(juniors_url)
        load_status=0
        while load_status!=200:
            load_status = r.status_code
        #print("\t##[Cantera Cargada]##")
        juniors = analyze_juniors(r.content)
        for j in juniors:
            if(db.juniors.find({"_id":j._id}).count() == 0):
                db.juniors.insert_one(j.to_db_collection())
            else:
                #print("\t-Ya existe-")
                db.juniors.replace_one({"_id":j._id},j.to_db_collection())
        for j in juniors:
            analyze_player_similars(j._id, False, None)

#-----Menu----
def option_one():
    """Option of web scrap the auctions on the actual market"""
    #Login
    login(auth)
    db.market.delete_many({})
    print('\t[Mercado previo eliminado]')

    params = {
        "juvenil": 0,
        "tiempos": TIME._24H.value,
        "posiciones": POSITION.ALL.value,
        "calidad": AVERAGE._86_90.value,
        "edad": -1,
        "cdirecta":  0
    }
    #Senior
    print('[Seniors]')
    for p_time in range(2,5):
        params['tiempos'] = p_time
        for p_avg in range(12,17):
            params['calidad'] = p_avg
            analyze_market_web(params)
    #Junior
    params['juvenil'] = 1
    params['edad'] = 0 #14 años
    for p_time in range(2,5):
        params['tiempos'] = p_time
        for p_avg in range(4,6):
            params['calidad'] = p_avg
            analyze_market_web(params)
        

def option_two():
    """Option of web scrap juniors from teams"""
    #Login
    login(auth)

    #Analyze divisions
    ## 1st division
    division = 1
    group = 1
    print('\t\t{Division 1}')
    analyze_teams_web(division, group)

    ## 2nd division
    login(auth)
    division = 2
    print('\t\t{Division 2}')
    for group in range(1,5):
        analyze_teams_web(division, group)
    
    ## 3rd division
    
    division = 3
    print('\t\t{Division 3}')
    for group in range(1,17):
        login(auth)
        analyze_teams_web(division, group)

def option_three():
    """Option of web scrap the statistics lines of a game"""
    path = input("Introduce la ruta del fichero html: ")
    fichero = open(path,'r', encoding="utf8")

    html_str = fichero.read()
    aus = analyze_game(html_str)
    #db.market.delete_many({}) 
    #for a in aus:
    #    print("\t{}".format(a))
    #    db.market.insert(a.to_db_collection())
    fichero.close

#========================
#--**--**--Main--**--**--
#========================

#Login
if os.path.isfile('./fich/user.xml'):
    login_file = open("./fich/user.xml",'r', encoding="utf8")
    login_str = login_file.read()
    alias = login_str[login_str.find('<alias>')+7:login_str.find('</alias>')]
    password = login_str[login_str.find('<pass>')+6:login_str.find('</pass>')]
    season = login_str[login_str.find('<season>')+8:login_str.find('</season>')]
    mongoClient_str = login_str[login_str.find('<mongodb>')+9:login_str.find('</mongodb>')]
    login_file.close
    print("[Login almacenado con exito]")
else:
    print("\n**Login IBM Web Scraper**")
    alias = input("\nIntroduce tu Alias:")
    password = getpass.getpass("\nIntroduce tu Contraseña:")
    season = input("\nIntroduce temporada actual:")
    mongoClient_str = 'mongodb://localhost:27017/'

auth={"alias":alias,"pass":password,"dest":None}

mongoClient = MongoClient(mongoClient_str)
db = mongoClient.ibm_web_scraper

session = requests.session()

#Menu
while True:
    os.system('cls')
    print("\n**IBM Web Scraper**")
    opcion = input("\nIntroduce una opción:\n[1] Obtener Mercado\n[2] Obtener Cantera\n[3] Analizar Partido \n\n[0] Salir del programa\n\n> ")

    if opcion == "1":
        option_one()

    elif opcion == "2":
        option_two()

    elif opcion == "3":
        option_three()
        pass

    elif opcion == "0":
        print("Cerrando programa!")
        os.system('cls')
        break

    else:
        print("Opción incorrecta")
    input("\nPulse para continuar...")