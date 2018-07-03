# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

import os
import getpass
import requests

from pymongo import MongoClient
from enum import Enum
from requests.auth import HTTPBasicAuth


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

session = requests.session()
