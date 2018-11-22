# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

from bs4 import BeautifulSoup

import re
import requests

def analyze_shop(html_content):
  soup = BeautifulSoup(html_content, 'html.parser')
  table_stock = soup.find('div', {"class": "tienda_stats_tables"}) #Llaveros
  tds = table_stock.find_all('td')
  #print(table_stock)
  llaveros = {
    "stock":int(str(tds[1])[str(tds[1]).find('<td>')+4:str(tds[1]).find('</td>')].replace(',',''))#,
    #"ayer":int(str(tds[7])[str(tds[7]).find('<td>')+4:str(tds[7]).find('</td>')].replace(',','')),
    #"semana":int(str(tds[13])[str(tds[13]).find('<td>')+4:str(tds[13]).find('</td>')].replace(',',''))
  }
  print(llaveros)
  banderolas = {
    "stock":int(str(tds[2])[str(tds[2]).find('<td>')+4:str(tds[2]).find('</td>')].replace(',',''))#,
    #"ayer":int(str(tds[8])[str(tds[8]).find('<td>')+4:str(tds[8]).find('</td>')].replace(',','')),
    #"semana":int(str(tds[14])[str(tds[14]).find('<td>')+4:str(tds[14]).find('</td>')].replace(',',''))
  } 
  print(banderolas)
  balones = {
    "stock":int(str(tds[3])[str(tds[3]).find('<td>')+4:str(tds[3]).find('</td>')].replace(',',''))#,
    #"ayer":int(str(tds[9])[str(tds[9]).find('<td>')+4:str(tds[9]).find('</td>')].replace(',','')),
    #"semana":int(str(tds[15])[str(tds[15]).find('<td>')+4:str(tds[15]).find('</td>')].replace(',',''))
  } 
  print(balones)
  camisetas = {
    "stock":int(str(tds[4])[str(tds[4]).find('<td>')+4:str(tds[4]).find('</td>')].replace(',',''))#,
    #"ayer":int(str(tds[10])[str(tds[10]).find('<td>')+4:str(tds[10]).find('</td>')].replace(',','')),
    #"semana":int(str(tds[16])[str(tds[16]).find('<td>')+4:str(tds[16]).find('</td>')].replace(',',''))
  } 
  print(camisetas)
  zapatillas = {
    "stock":int(str(tds[5])[str(tds[5]).find('<td>')+4:str(tds[5]).find('</td>')].replace(',',''))#,
    #"ayer":int(str(tds[11])[str(tds[11]).find('<td>')+4:str(tds[11]).find('</td>')].replace(',','')),
    #"semana":int(str(tds[17])[str(tds[17]).find('<td>')+4:str(tds[17]).find('</td>')].replace(',',''))
  } 
  print(zapatillas)
  return [llaveros, banderolas, balones, camisetas, zapatillas]
  

def automate_test(html_content,auth, shop_stock):
  session = requests.session()
  print("\n")
  print(shop_stock[4])
  min_stock = shop_stock[4]["stock"]
  order = 5
  if shop_stock[3]["stock"] <= min_stock:
    min_stock = shop_stock[3]["stock"]
    order = 4
  if shop_stock[2]["stock"] <= min_stock:
    min_stock = shop_stock[2]["stock"]
    order = 3
  if shop_stock[1]["stock"] <= min_stock:
    min_stock = shop_stock[1]["stock"]
    order = 2
  if shop_stock[0]["stock"] <= min_stock:
    min_stock = shop_stock[0]["stock"]
    order = 1
  print(order)
  return order
  
  #print(BeautifulSoup(r.content, 'html.parser'))