# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

from market.auction import *

import re
import datetime

reg_day = '(Lunes|Martes|Miércoles|Jueves|Viernes|Sábado|Domingo),'
reg_hour = '(([01]\d|2[0-3]):([0-5]\d)|24:00)'

def analyze_market(html_str):
    """Analyze the html page of Market.
    
    Return an array of auctions

    Keyword arguments:
    html_str -- Full text of the webpage of market in string format.
        The web page direction is similar at :
        /mercado.php?juvenil=0&tiempos=2&posiciones=-1&calidad=14&edad=-1&cdirecta=0&
    """
    #table_str = html_str[html_str.find('<thead>')+7:html_str.find('</table>',1)]
    table_str = html_str[html_str.find('</thead>')+8:]
    table_str = table_str[:table_str.find('</table>')+8]
    players = table_str.replace('\n', '').replace('\t', '').split('<tr')
    auctions = []
    for player_str in players[1:]:
        data_player = player_str.split('<td')
        #print("****\n")
        #print(data_player[9])
        #for dat in data_player:
        #    print("\n" + dat)
        url = data_player[2][data_player[2].find('&id_jugador=')+12:data_player[2].find('" >')]
        pos = data_player[3][data_player[3].find('</div>')+6:data_player[3].find('</td>')]
        avg = data_player[4][data_player[4].find('>')+1:data_player[4].find('</td>')]
        age = data_player[5][data_player[5].find('>')+1:data_player[5].find('</td>')]
        date_auction = date_translation(data_player[7][data_player[7].find('</div>')+6:data_player[7].find('</td>')])
        offer = data_player[9][data_player[9].find('right;">')+8:data_player[9].find('&nbsp;&euro;')]
        #print(date_auction)

        auctions.append(Auction(url,pos,avg,age,date_auction,offer))
    
    return auctions

def date_translation(html_str):
    """Transform short date format to standard date format.

    Keyword arguments:
    html_str -- String who represents a date in diverse formats.
    """
    html_str = html_str.replace('&nbsp;',' ').replace('&aacute;','á').replace('&eacute;','é').replace('&iacute;','í').replace('&oacute;','ó').replace('&uacute;','ú')
    hr=re.search(reg_hour,html_str).group(0)
    #print(html_str)
    hour=int(hr.split(':')[0])
    minutes=int(hr.split(':')[1])
    #print('{}:{}'.format(hour,minutes))
    today = datetime.datetime.today()
    if(re.search(reg_day,html_str) is not None):
        h = html_str.split(' ')
        while(int(today.strftime("%d")) != int(h[1])):
            today = today + datetime.timedelta(days=1)
    elif(re.search('Mañana',html_str) is not None):
        today = today + datetime.timedelta(days=1)
    elif(re.search('Hoy',html_str) is not None):
        pass
    else:
        print('COMPROBAR')
    today = today.replace(
        hour=hour,
        minute=minutes
    )
    return today

#Main
#path = input("Introduce la ruta del fichero html: ")
#fichero = open(path,'r', encoding="utf8")

#html_str = fichero.read()
#analyze_webpage(html_str)