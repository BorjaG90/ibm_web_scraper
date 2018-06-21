# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

import os

from pymongo import MongoClient

def analyze():
  elements = db.market.find()
  for p in elements:
    offer_max = int(p['offer'] * 1.05)
    similar_buys = db.transactions.find({"age":p['age'], "average":p['average'],"position":p['position']})
    avg_clause = 0
    count_clause = 0
    s_clause =0
    avg_auction = 0
    count_auction = 0
    s_auction = 0 
    avg_direct = 0
    count_direct = 0
    s_direct = 0
    for t in similar_buys:
      if(str(t['type_buy']) == 'Clausulazo'):
        avg_clause += int(t['price'])
        count_clause += 1 
      elif(str(t['type_buy']) == 'Subasta'):
        avg_auction += int(t['price'])
        count_auction += 1
      else:
        avg_direct += int(t['price'])
        count_direct += 1
    if(count_auction>0):
      s_auction = avg_auction / count_auction
    if(count_clause>0):
      s_clause = avg_clause / count_clause
    if(count_direct>0):
      s_direct = avg_direct / count_direct
    offer_max = int(p['offer'] * 1.10)
    if(s_auction >= offer_max or s_clause >= offer_max or s_direct >= offer_max):
      print("Offer: " + str(p['offer']) + "€ : " +p['position']+"/"+str(p['age'])+"/"+str(p['average'])+" Max offer: "+str(offer_max))
      msg = "\t[http://es.ibasketmanager.com/jugador.php?id_jugador="+str(p['_id'])+"] :"
      msg = msg+str(p['offer'])+"€, Sub:"+str(s_auction)+"€, Claus:"+str(s_clause)+"€, Dir:"+str(s_direct)
      print(msg)


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

mongoClient = MongoClient(mongoClient_str)
db = mongoClient.ibm_web_scraper

analyze()

