# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

from roster.roster import *
from bs4 import BeautifulSoup

import re
import datetime

reg_day = '(Lunes|Martes|Miércoles|Jueves|Viernes|Sábado|Domingo),'
reg_hour = '(([01]\d|2[0-3]):([0-5]\d)|24:00)'

def analyze_roster_senior(html_content):
    """Analyze the html page of Senior Roster.
    
    Return an array of player_urls

    Keyword arguments:
    html_content -- Full text of the webpage of senior roster in string format.
        The web page direction is similar at :
        /plantilla.php?juvenil=1&id_equipo=114
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    final = soup.find_all('table', {"id": "pagetabla"}) #Dont have Juniors
    mensaje = soup.find('div',{"id": "menserror"}) #Playing a game
    seniors = []
    if(final!=None and mensaje == None): 
        seniors_str = soup.find_all('table', {"id": "pagetabla"})[0].find_all('tr')
        seniors_str.pop(0)
        
        for senior_str in seniors_str:
            senior_soup = BeautifulSoup(str(senior_str),'html.parser')
            data_senior = senior_soup.find_all('td')
            url = str(data_senior[2])[str(data_senior[2]).find('id_jugador=')+11:
                str(data_senior[2]).find('">',str(data_senior[2]).find('id_jugador=')+11)]
            pos = str(data_senior[3])[str(data_senior[3]).find('</div>')+6:str(data_senior[3]).find('</td>')]
            seniors.append([url,pos])
    return seniors

def analyze_senior_player(html_content, id):
    """Analyze the html page of a Senior Player.
    
    Return an array of teams_urls

    Keyword arguments:
    html_content -- Full text of the webpage of senior in string format.
        The web page direction is similar at :
        jugador.php?id_jugador=5292302
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    final = soup.find_all('div', {"class": "resumenjugadorPP"}) #Dont have Atts
    mensaje = soup.find('div',{"id": "menserror"}) #Playing a game
    attributes = []
    if(final!=None and mensaje == None): 
        first = final[0].find('table')
        bars1 = first.find_all('div',{"class": "jugbarranum"})

        attributes.append(bars1[0].find(text=True, recursive=False))
        attributes.append(bars1[1].find(text=True, recursive=False))
        attributes.append(0)
        attributes.append(bars1[2].find(text=True, recursive=False))
        attributes.append(bars1[3].find(text=True, recursive=False))
        attributes.append(bars1[4].find(text=True, recursive=False))
        attributes.append(bars1[5].find(text=True, recursive=False))
        attributes.append(bars1[6].find(text=True, recursive=False))
        lvl = bars1[7].find(text=True, recursive=False)
        lvl = str(lvl).replace(' (Niv. ',':').replace(')','').replace(',','')
        if(lvl.split(':')[1] == ''):
            attributes.append(0)
        else:
            attributes.append(lvl.split(':')[1])
        attributes.append(lvl.split(':')[0])

        second = final[1].find('table')
        bars2 = second.find_all('div',{"class": "jugbarranum"})

        attributes.append(bars2[0].find(text=True, recursive=False))
        attributes.append(bars2[1].find(text=True, recursive=False))
        attributes.append(bars2[2].find(text=True, recursive=False))
        attributes.append(bars2[3].find(text=True, recursive=False))
        attributes.append(bars2[4].find(text=True, recursive=False))
        attributes.append(bars2[5].find(text=True, recursive=False))
        attributes.append(bars2[6].find(text=True, recursive=False))
        attributes.append(bars2[7].find(text=True, recursive=False))
        attributes.append(bars2[8].find(text=True, recursive=False))
        attributes.append(bars2[9].find(text=True, recursive=False))
        attributes.append(bars2[10].find(text=True, recursive=False))
        attributes.append(0)

        # for b in bars:
        #     text = b.find(text=True, recursive=False)
        #     print(text)
    return attributes

def analyze_roster_junior(html_content):
    """Analyze the html page of Junior Roster.
    
    Return an array of player_urls

    Keyword arguments:
    html_content -- Full text of the webpage of senior roster in string format.
        The web page direction is similar at :
        /plantilla.php?juvenil=0&id_equipo=114
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    final = soup.find_all('table', {"id": "pagetabla"}) #Dont have Juniors
    mensaje = soup.find('div',{"id": "menserror"}) #Playing a game
    juniors = []
    if(final!=None and mensaje == None): 
        juniors_str = soup.find_all('table', {"id": "pagetabla"})[0].find_all('tr')
        juniors_str.pop(0)
        
        for junior_str in juniors_str:
            junior_soup = BeautifulSoup(str(junior_str),'html.parser')
            data_junior = junior_soup.find_all('td')
            url = str(data_junior[1])[str(data_junior[1]).find('id_jugador=')+11:
                str(data_junior[1]).find('">',str(data_junior[1]).find('id_jugador=')+11)]
            pos = str(data_junior[2])[str(data_junior[2]).find('</div>')+6:str(data_junior[2]).find('</td>')]
            juniors.append([url,pos])
    return juniors

def analyze_junior_player(html_content, id):
    """Analyze the html page of a Junior Player.
    
    Return an array of teams_urls

    Keyword arguments:
    html_content -- Full text of the webpage of senior in string format.
        The web page direction is similar at :
        jugador.php?id_jugador=5292302
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    final = soup.find_all('div', {"class": "resumenjugadorPP"}) #Dont have Atts
    mensaje = soup.find('div',{"id": "menserror"}) #Playing a game
    attributes = []
    if(final!=None and mensaje == None): 
        first = final[0].find('table')
        bars1 = first.find_all('div',{"class": "jugbarranum"})

        attributes.append(bars1[0].find(text=True, recursive=False))
        attributes.append(bars1[1].find(text=True, recursive=False))
        attributes.append(0)
        attributes.append(bars1[2].find(text=True, recursive=False))
        attributes.append(bars1[3].find(text=True, recursive=False))
        attributes.append(bars1[4].find(text=True, recursive=False))
        attributes.append(bars1[5].find(text=True, recursive=False))
        attributes.append(bars1[6].find(text=True, recursive=False))
        lvl = bars1[7].find(text=True, recursive=False)
        lvl = str(lvl).replace(' (Niv. ',':').replace(')','').replace(',','')
        if(lvl.split(':')[1] == ''):
            attributes.append(0)
        else:
            attributes.append(lvl.split(':')[1])
        attributes.append(lvl.split(':')[0])

        second = final[1].find('table')
        bars2 = second.find_all('div',{"class": "jugbarranum"})

        attributes.append(bars2[0].find(text=True, recursive=False))
        attributes.append(bars2[1].find(text=True, recursive=False))
        attributes.append(bars2[2].find(text=True, recursive=False))
        attributes.append(bars2[3].find(text=True, recursive=False))
        attributes.append(bars2[4].find(text=True, recursive=False))
        attributes.append(bars2[5].find(text=True, recursive=False))
        attributes.append(bars2[6].find(text=True, recursive=False))
        attributes.append(bars2[7].find(text=True, recursive=False))
        attributes.append(bars2[8].find(text=True, recursive=False))
        attributes.append(bars2[9].find(text=True, recursive=False))
        attributes.append(bars2[10].find(text=True, recursive=False))

        # for b in bars:
        #     text = b.find(text=True, recursive=False)
        #     print(text)
    return attributes

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
    elif(re.search('Mañana',html_content) is not None):
        today = today + datetime.timedelta(days=1)
    elif(re.search('Hoy',html_content) is not None):
        pass
    else:
        print('\t[Roster-COMPROBAR]:' + html_content)
    today = today.replace(
        hour=hour,
        minute=minutes
    )
    return today