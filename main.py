# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

import os

from pymongo import MongoClient
from transfers.readWebPage import *
from market.readWebPage import *

def option_one():
    """Option of web scrap similar buys of a player"""
    path = input("Introduce la ruta del fichero html: ")
    fichero = open(path,'r', encoding="utf8")

    html_str = fichero.read()

    ts = analyze_similar_buys(html_str)
    for t in ts:
        print("\t{}".format(t))
        if(
            db.transactions.find(
                {"_id_player":t._id_player}, 
                {"_id_date_buy":t._id_date_buy}
            ).count() == 0
        ):
            db.transactions.insert(t.to_db_collection())
        else:
            print("\t-Ya existe-")
    fichero.close

def option_two():
    """Option of web scrap the auctions on the actual market"""
    path = input("Introduce la ruta del fichero html: ")
    fichero = open(path,'r', encoding="utf8")

    html_str = fichero.read()
    aus = analyze_market(html_str)
    db.market.delete_many({}) 
    for a in aus:
        print("\t{}".format(a))
        db.market.insert(a.to_db_collection())
    fichero.close

#Main
mongoClient = MongoClient('localhost',27017)
db = mongoClient.ibm_web_scraper

#Menu
while True:
    os.system('cls')
    print("\n**IBM Web Scraper**")
    opcion = input("\nIntroduce una opción:\n[1] Obtener Compras Similares\n[2] Obtener Mercado\n\n[0] Salir del programa\n\n> ")

    if opcion == "1":
        option_one()

    elif opcion == "2":
        option_two()

    elif opcion == "3":
        #mostrar_menu()
        pass

    elif opcion == "0":
        print("Cerrando programa!")
        os.system('cls')
        break

    else:
        print("Opción incorrecta")
    input("\nPulse para continuar...")
    

