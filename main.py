# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

import os
import getpass
import requests

from pymongo import MongoClient
from enum import Enum
from requests.auth import HTTPBasicAuth
#from lxml import html

from transfers.readWebPage import *
from market.readWebPage import *
from market.bid import *
from statistics.readWebPage import *
from roster.readWebPage import *
from team.readWebPage import *
from team.team import *

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

#--Functions--

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
    print(transactions_url)
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
    #for a in aus:
        #analyze_player_similars(a._id, False, None)

def analyze_juniors_web(division, group):
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
                db.juniors.delete_one({"_id":j._id})
                db.juniors.insert_one(j.to_db_collection())
        # for j in juniors:
        #     analyze_player_similars(j._id, False, None)

def analyze_roster_web(division, group):
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
        roster_url = url + 'plantilla.php?id_equipo=' + team_url
        print('  - Equipo ' + team_url +' :[ ' + roster_url + ' ]')
        
        r = session.get(roster_url)
        load_status=0
        while load_status!=200:
            load_status = r.status_code
        #print("\t##[Cantera Cargada]##")
        roster = analyze_seniors(r.content)
        for p in roster:
            if(db.seniors.find({"_id":p._id}).count() == 0):
                db.seniors.insert_one(p.to_db_collection())
            else:
                #print("\t-Ya existe-")
                db.seniors.delete_one({"_id":p._id})
                db.seniors.insert_one(p.to_db_collection())
        # for p in roster:
        #     analyze_player_similars(p._id, False, None)

def analyze_own_team(id_team):
    roster_url = url + 'plantilla.php?id_equipo=' + str(id_team)
    print(' >{ ' + roster_url + ' }')
    r = session.get(roster_url)
    load_status=0
    while load_status!=200:
        load_status = r.status_code
    print("[Seniors]")
    seniors = analyze_roster_senior(r.content)
    for s in seniors:
        senior_url = url + 'jugador.php?id_jugador=' + s[0]
        print('  - Senior ' + s[0] +' :[ ' + senior_url + ' ]')

        r = session.get(senior_url)
        load_status=0
        while load_status!=200:
            load_status = r.status_code
        attr = analyze_senior_player(r.content, url)
        player = Senior_Team(
            s[0],
            s[1],
            attr[0],
            attr[1],
            attr[2],
            attr[3],
            attr[4],
            attr[5],
            attr[6],
            attr[7],
            attr[8],
            attr[9],
            attr[10],
            attr[11],
            attr[12],
            attr[13],
            attr[14],
            attr[15],
            attr[16],
            attr[17],
            attr[18],
            attr[19],
            attr[20],
            attr[21]
            )
        if(db.team.find({"_id":player._id}).count() == 0):
            db.team.insert_one(player.to_db_collection())
        else:
            #print("\t-Ya existe-")
            db.team.replace_one({"_id":player._id},player.to_db_collection())

    roster_url = url + 'plantilla.php?juveniles=1&id_equipo=' + str(id_team)
    print(' >{ ' + roster_url + ' }')
    r = session.get(roster_url)
    load_status=0
    while load_status!=200:
        load_status = r.status_code
    print("[Juniors]")
    juniors = analyze_roster_junior(r.content)
    for s in juniors:
        junior_url = url + 'jugador.php?id_jugador=' + s[0]
        print('  - Junior ' + s[0] +' :[ ' + senior_url + ' ]')

        r = session.get(junior_url)
        load_status=0
        while load_status!=200:
            load_status = r.status_code
        attr = analyze_junior_player(r.content, url)
        player = Junior_Team(
            s[0],
            s[1],
            attr[0],
            attr[1],
            attr[2],
            attr[3],
            attr[4],
            attr[5],
            attr[6],
            attr[7],
            attr[8],
            attr[9],
            attr[10],
            attr[11],
            attr[12],
            attr[13],
            attr[14],
            attr[15],
            attr[16],
            attr[17],
            attr[18],
            attr[19],
            attr[20]
            )
        if(db.team.find({"_id":player._id}).count() == 0):
            db.team.insert_one(player.to_db_collection())
        else:
            #print("\t-Ya existe-")
            db.team.replace_one({"_id":player._id},player.to_db_collection())
        

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
        for p_avg in range(7,17):
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
    analyze_juniors_web(division, group)

    ## 2nd division
    login(auth)
    division = 2
    print('\t\t{Division 2}')
    for group in range(1,5):
        analyze_juniors_web(division, group)
    
    ## 3rd division
    division = 3
    print('\t\t{Division 3}')
    for group in range(1,17):
        login(auth)
        analyze_juniors_web(division, group)

def option_three():
    """Option of web scrap roster from division 1, 2 & 3 teams"""
    #Login
    login(auth)

    #Analyze divisions
    ## 1st division
    division = 1
    group = 1
    print('\t\t{Division 1}')
    analyze_roster_web(division, group)

    ## 2nd division
    login(auth)
    division = 2
    print('\t\t{Division 2}')
    for group in range(1,5):
        analyze_roster_web(division, group)
    
    ## 3rd division
    division = 3
    print('\t\t{Division 3}')
    for group in range(1,17):
        login(auth)
        analyze_roster_web(division, group)

def option_four():
    """Option of web scrap juniors from division 4 teams"""
    #Login
    login(auth)

    #Analyze divisions
    ## 4th division
    division = 4
    print('\t\t{Division 4}')
    for group in range(1,65):
        login(auth)
        analyze_juniors_web(division, group)

def option_five():
    """Option of web scrap seniors from division 4 teams"""
    #Login
    login(auth)

    #Analyze divisions
    ## 4th division
    division = 4
    print('\t\t{Division 4}')
    for group in range(1,65):
        login(auth)
        analyze_roster_web(division, group)

def option_six():
    """Option of analize a single example of each combination and obtain his similars transactions""" 
    min_j_age = db.juniors.find().sort([("age", 1)]).limit(1)[0]['age']
    max_j_age = db.juniors.find().sort([("age", -1)]).limit(1)[0]['age']
    min_j_avg = db.juniors.find().sort([("average", 1)]).limit(1)[0]['average']
    max_j_avg = db.juniors.find().sort([("average", -1)]).limit(1)[0]['average']
    min_s_age = db.seniors.find().sort([("age", 1)]).limit(1)[0]['age']
    max_s_age = db.seniors.find().sort([("age", -1)]).limit(1)[0]['age']
    min_s_avg = db.seniors.find().sort([("average", 1)]).limit(1)[0]['average']
    max_s_avg = db.seniors.find().sort([("average", -1)]).limit(1)[0]['average']
    positions = ['B','E','A','AP','P']
    examples = []
    # Obtain a example of every combination of players
    for i in range(0,len(positions)):
        login(auth)
        position = positions[i]
        for j in range(min_j_age, max_j_age +1):
            print("J Age: " + str(j) + " " + position)
            for k in range(min_j_avg, max_j_avg +1):
                elements = db.juniors.find({"position":position,"age":j,"average":k}).limit(3)
                for element in elements:
                    if(element!=None):
                        examples.append(element)
        for j in range(min_s_age, max_s_age +1):
            print("S Age: " + str(j) + " " + position)
            for k in range(min_s_avg, max_s_avg +1):
                element = db.seniors.find({"position":position,"age":j,"average":k}).limit(3)
                for element in elements:
                    if(element!=None):
                        examples.append(element)

    # Obtain similar buys
    for player in examples:
        analyze_player_similars(player['_id'], False, None)
    
def option_seven():
    """Option of web scrap the attributes of your own team and juniors""" 
    #Login
    login(auth)

    analyze_own_team(14612)

def option_eight():
    """ Option of auto bid in an auction for a player """
    #Login
    login(auth)

    play_aut_id = input("Introduce el id del jugador: ")
    bid_url = url + 'ofertapuja.php?acc=nuevo&id_jugador=' + str(play_aut_id)
    #http://es.ibasketmanager.com/ofertapuja.php?acc=nuevo&id_jugador=6345048
    print(' >{ ' + bid_url + ' }')
    r = session.get(bid_url)
    load_status=0
    while load_status!=200:
        load_status = r.status_code
    #make_bid(r.content,play_aut_id,auth)

    ###########################################################
    soup = BeautifulSoup(r.content, 'html.parser')
    final = soup.find("span",{"id":"claus"})
    # print(final)
    if(final!=None): #I can bid
        puja = final.find(text=True, recursive=False)
        puja_max = soup.find("span",{"id":"clausmax"}).find(text=True, recursive=False)
        fich = soup.find_all("div",{"class":"selector2"})[2].attrs['valor']
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
        "id_jugador":str(play_aut_id),
        "clausula":str(puja),
        "clausulamax":str(max_team),
        "ficha":str(max_player),
        "anos":str(years)
        }
        login(auth)

        bid_up = 5000
        if(int(max_player)-int(fich) < 5000):
            print("Apuestas a 100")
            bid_up = 100
        elif(int(max_player)-int(fich) < 25000):
            print("Apuestas a 1000")
            bid_up = 1000
        for i in range(int(fich),int(max_player)+1,bid_up):

            print(" Bid: [" + str(i) + "€]")

            x_url = "http://es.ibasketmanager.com/ofertapuja.php?acc=" + par['acc']
            x_url = x_url + "&tipo=" + par['tipo'] + "&id_jugador=" + par['id_jugador']
            x_url = x_url + "&clausula=" + par['clausula'] + "&clausulamax=" + par['clausulamax']
            x_url = x_url + "&ficha=" + str(i) + "&anos=" + par['anos']
            # print(x_url)
            r = session.post(x_url)
            load_status=0
            while load_status!=200:
                load_status = r.status_code
            soup=BeautifulSoup(r.content, 'html.parser')
            # print('#########')
            # print(str(soup))
            # print('#########')
            final = soup.find("td",{"class":"formerror"})
            #print(final.find(text=True, recursive=False))
            if(final==None):
                print("La apuesta es buena")
                print(final.find(text=True, recursive=False))
                i=int(max_player+1)
        print("Fin de bucle")
    else:
        print("No puedes pujar por este jugador")

def option_nine():
    """ Option of auto renove for a player """
    #Login
    login(auth)
    
    play_aut_id = input("Introduce el id del jugador: ")
    bid_url = url + 'ofertarenovar.php?acc=nuevo&tipo=4&id_jugador=' + str(play_aut_id)
    #http://es.ibasketmanager.com/ofertarenovar.php?acc=nuevo&tipo=4&id_jugador=7895726
    print(' >{ ' + bid_url + ' }')
    r = session.get(bid_url)
    load_status=0
    while load_status!=200:
        load_status = r.status_code
    #make_bid(r.content,play_aut_id,auth)

    ###########################################################
    soup = BeautifulSoup(r.content, 'html.parser')
    #print(soup)
    final = soup.find_all("div",{"class":"selector2"})[0].attrs['valor']
    print(final)
    if(final!=None): #I can bid
        fich = soup.find_all("div",{"class":"selector2"})[0].attrs['valor']
        ano = soup.find("span",{"id":"ano"}).find(text=True, recursive=False)
        print("Ficha: " + str(fich))
        print("Años: " + str(ano))

        min_player = input("Introduzca Ficha máxima para el Jugador: ")
        max_player = input("Introduzca Ficha máxima para el Jugador: ")
        years = input("Introduzca Años de Contrato: ")

        par = {
        "acc":"ofrecer",
        "tipo":"4",
        "id_jugador":str(play_aut_id),
        "clausula":str(0),
        "clausulamax":str(0),
        "ficha":str(max_player),
        "anos":str(years)
        }
        login(auth)

        bid_up = 5000
        if(int(max_player)-int(min_player) < 5000):
            print("Apuestas a 100")
            bid_up = 100
        elif(int(max_player)-int(min_player) < 25000):
            print("Apuestas a 1000")
            bid_up = 1000
        for i in range(int(min_player),int(max_player)+1,bid_up):

            print(" Bid: [" + str(i) + "€]")

            x_url = "http://es.ibasketmanager.com/ofertarenovar.php?acc=" + par['acc']
            x_url = x_url + "&tipo=" + par['tipo'] + "&id_jugador=" + par['id_jugador']
            x_url = x_url + "&clausula=" + par['clausula'] + "&clausulamax=" + par['clausulamax']
            x_url = x_url + "&ficha=" + str(i) + "&anos=" + par['anos']
            print(x_url)
            r = session.post(x_url)
            load_status=0
            while load_status!=200:
                load_status = r.status_code
            soup=BeautifulSoup(r.content, 'html.parser')
            # print('#########')
            # print(str(soup))
            # print('#########')
            final = soup.find("td",{"class":"formerror"})
            #print(final.find(text=True, recursive=False))
            if(final==None):
                print("La apuesta es buena")
                print(final.find(text=True, recursive=False))
                i=int(max_player+1)
        print("Fin de bucle")
    else:
        print("No puedes renovar este jugador")

def option_number():
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
    print("\n[1] Obtener Mercado\n[2] Obtener Cantera(Division 1,2 & 3)")
    print("[3] Obtener Plantillas (Division 1, 2 & 3)")
    print("[4] Obtener Cantera (Division 4)")
    print("[5] Obtener Plantilla (Division 4)")
    print("[6] Obtener transacciones")
    print("[7] Obtener atributos")
    print("[8] Apuesta automatica por un jugador")
    print("[9] Renovación automatica por un jugador")
    print("[A] Realizar todo")
    print("[B] Realizar todo sin transacciones")
    print("\n[0] Salir del programa\n")
    opcion = input("Introduce una opción: > ")

    if opcion == "1":
        option_one()

    elif opcion == "2":
        option_two()

    elif opcion == "3":
        option_three()

    elif opcion == "4":
        option_four()

    elif opcion == "5":
        option_five()
    
    elif opcion == "6":
        option_six()

    elif opcion == "7":
        option_seven()

    elif opcion == "8":
        option_eight()
    
    elif opcion == "9":
        option_nine()

    elif opcion == "A":
        option_one()
        option_two()
        option_three()
        option_four()
        option_five()
        option_six()
    
    elif opcion == "B":
        option_one()
        option_two()
        option_three()
        option_four()
        option_five()
        
    elif opcion == "0":
        print("Cerrando programa!")
        os.system('cls')
        break

    else:
        print("Opción incorrecta")
    input("\nPulse para continuar...")