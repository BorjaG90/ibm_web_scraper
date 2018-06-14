# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

from market.auction import *
from bs4 import BeautifulSoup

import re
import datetime

reg_day = '(Lunes|Martes|Miércoles|Jueves|Viernes|Sábado|Domingo),'
reg_hour = '(([01]\d|2[0-3]):([0-5]\d)|24:00)'

def analyze_market(html_content):
    """Analyze the html page of Market.
    
    Return an array of auctions

    Keyword arguments:
    html_content -- Full text of the webpage of market in string format.
        The web page direction is similar at :
        /mercado.php?juvenil=0&tiempos=2&posiciones=-1&calidad=14&edad=-1&cdirecta=0&
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    auctions = []
    final = soup.find('div',{'class':'texto final'})
    if(final==None): #If there is auctions with that filter
        players_str = soup.find_all('table', {"id": "pagetabla"})[0].find_all('tr')
        players_str.pop(0)
        # print(players_str)
        
        for player_str in players_str:
            player_soup = BeautifulSoup(str(player_str),'html.parser')
            data_player = player_soup.find_all('td')
            url = str(data_player[1])[str(data_player[1]).find('id_jugador=')+11:
                str(data_player[1]).find('">',str(data_player[1]).find('id_jugador=')+11)]
            pos = str(data_player[2])[str(data_player[2]).find('</div>')+6:str(data_player[2]).find('</td>')]
            avg = str(data_player[3])[str(data_player[3]).find('>')+1:str(data_player[3]).find('</td>')]
            age = str(data_player[4])[str(data_player[4]).find('>')+1:str(data_player[4]).find('</td>')]
            date_auction = date_translation(str(data_player[6])[str(data_player[6]).find('</div>')+6:str(data_player[6]).find('</td>')])
            offer = str(data_player[8])[str(data_player[8]).find('right;">')+8:str(data_player[8]).find('</td')-2]
            auctions.append(Auction(url,pos,avg,age,date_auction,offer))
    else:
        print('\t' + final.contents[0])
    return auctions

def date_translation(html_content):
    """Transform short date format to standard date format.

    Keyword arguments:
    html_content -- String who represents a date in diverse formats.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    html_content = str(soup).replace('&nbsp;',' ').replace('&aacute;','á').replace('&eacute;','é').replace('&iacute;','í').replace('&oacute;','ó').replace('&uacute;','ú')
    hr=re.search(reg_hour,html_content).group(0)
    #print(html_content)
    hour=int(hr.split(':')[0])
    minutes=int(hr.split(':')[1])
    #print('{}:{}'.format(hour,minutes))
    today = datetime.datetime.today()
    if(re.search(reg_day,html_content) is not None):
        h = str(html_content).split('\xa0')
        while(int(today.strftime("%d")) != int(h[1])):
            today = today + datetime.timedelta(days=1)
    elif(re.search('MaÃ±ana',html_content) is not None or re.search('Mañana',html_content) is not None):
        today = today + datetime.timedelta(days=1)
    elif(re.search('Hoy',html_content) is not None):
        pass
    else:
        print('\t[Market-COMPROBAR]:' + html_content)
    today = today.replace(
        hour=hour,
        minute=minutes
    )
    return today