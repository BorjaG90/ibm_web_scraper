# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

from transfers.transaction import *

import re
import datetime

reg_month = '(Ene|Feb|Mar|Abr|May|Jun|Jul|Ago|Sep|Oct|Nov|Dic)'
reg_day = '(Lunes|Martes|Miércoles|Jueves|Viernes|Sábado|Domingo)'
reg_date_full = '(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]|(?:Jan|Mar|May|Jul|Aug|Oct|Dec)))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2]|(?:Jan|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)(?:0?2|(?:Feb))\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9]|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep))|(?:1[0-2]|(?:Oct|Nov|Dec)))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})'


def analyze_similar_buys(html_str):
    """Analyze the html page of Similar Buys of a player.
    
    Return an array of transactions

    Keyword arguments:
    html_str -- Full text of the webpage of similar buys in string format.
        The web page direction is similar at :
        /jugador_compras_similares.php?id_jugador=xxxxxxx
    """
    table_str = html_str[html_str.find('<tbody class="pijama">')+22:html_str.find('</tbody>')-8]
    players = table_str.replace('\n', '').replace('\t', '').split('<tr')
    transactions = []
    for player_str in players[1:]:
        data_player = player_str.split('<td')
        
        url = data_player[1][data_player[1].find('href="')+6:data_player[1].find('">')]
        #print(url)
        id_player = url[url.find('?id_jugador=')+12:] 
        name = data_player[1][data_player[1].find('">')+2:data_player[1].find('</a>')]
        id_date_buy = data_player[2][data_player[2].find('none;">')+7:data_player[2].find('</div>')]
        date_buy = date_translation(data_player[2][data_player[2].find('</div>')+6:data_player[2].find('</td>')])
        age = data_player[3][data_player[3].find('">')+2:data_player[3].find('</td>')]
        avg = data_player[4][data_player[4].find('">')+2:data_player[4].find('</td>')]
        pos = data_player[5][data_player[5].find('">')+2:data_player[5].find('</td>')]
        salary = data_player[6][data_player[6].find('">')+2:data_player[6].find('&euro;')]
        price = data_player[7][data_player[7].find('">')+2:data_player[7].find('&euro;')]
        type_buy = data_player[8][data_player[8].find('">')+2:data_player[8].find('</td>')]

        #print('Id: '+ id_player + ' Jugador: ' + name+ ' ' + pos +  ' de ' + age + ' años, con ' + avg + ' de media')
        #print('Vendido en ' + type_buy + ' por ' + price + '€, cobrando ' + salary + '€ en la fecha '+ id_date_buy +'\n')
        
        transactions.append(
            Transaction(
                id_player, 
                id_date_buy, 
                age, 
                avg, 
                pos, 
                price, 
                type_buy, 
                salary, 
                date_buy
            )
        )
    return transactions


def date_translation(html_str):
    """Transform short date format to standard date format.

    Keyword arguments:
    html_str -- String who represents a date in diverse formats.
    """
    # Remove the hour
    html_str = html_str.replace(re.search('\s\d{1,2}:\d{1,2}',html_str).group(0),'')
    if(re.search(reg_month,html_str) is not None):
        day = re.search('\d{1,2}',html_str).group(0).replace(' ','')
        month_str = re.search(reg_month,html_str).group(0)
        if(month_str == 'Ene'):
            month = 1
        elif(month_str == 'Feb'):
            month = 2
        elif(month_str == 'Mar'):
            month = 3
        elif(month_str == 'Abr'):
            month = 4
        elif(month_str == 'May'):
            month = 5
        elif(month_str == 'Jun'):
            month = 6
        elif(month_str == 'Jul'):
            month = 7
        elif(month_str == 'Ago'):
            month = 8
        elif(month_str == 'Sep'):
            month = 9
        elif(month_str == 'Oct'):
            month = 10
        elif(month_str == 'Nov'):
            month = 11
        elif(month_str == 'Dic'):
            month = 12
        if(month < datetime.datetime.now().month):
            year = datetime.datetime.now().year -1
        else:
            year = datetime.datetime.now().year
        return '{}/{}/{}'.format(str(day).zfill(2),str(month).zfill(2),year)
    elif(re.search(reg_day,html_str) is not None):
        day = re.search('\d{1,2}',html_str).group(0).replace(' ','')
        if(int(day) < datetime.datetime.now().day):
            if(datetime.datetime.now().month == 1):
                month = 12
            else:
                month = datetime.datetime.now().month -1
        else:
            month = datetime.datetime.now().month
        if(month < datetime.datetime.now().month):
            year = datetime.datetime.now().year -1
        else:
            year = datetime.datetime.now().year
        return '{}/{}/{}'.format(str(day).zfill(2),str(month).zfill(2),year)
    else:
        #print(html_str)
        return html_str