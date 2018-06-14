# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

from roster.roster import *
from bs4 import BeautifulSoup

import re
import datetime

reg_day = '(Lunes|Martes|Miércoles|Jueves|Viernes|Sábado|Domingo),'
reg_hour = '(([01]\d|2[0-3]):([0-5]\d)|24:00)'

def analyze_standings(html_content):
    """Analyze the html page of Standings.
    
    Return an array of teams_urls

    Keyword arguments:
    html_content -- Full text of the webpage of standings in string format.
        The web page direction is similar at :
        /liga.php?temporada=33?division=1&grupo=114
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    teams_str_a = soup.find_all('table')[0].find_all('a')
    teams_str_b = soup.find_all('table')[1].find_all('a')
    teams_urls = []
    for team_str in teams_str_a + teams_str_b:
        data_team = BeautifulSoup(str(team_str),'html.parser')
        url = str(data_team)[str(data_team).find('id=')+3:
            str(data_team).find('">',str(data_team).find('id=')+3)]
        teams_urls.append(url)
    return teams_urls

def analyze_juniors(html_content):
    """Analyze the html page of Junior Roster.
    
    Return an array of teams_urls

    Keyword arguments:
    html_content -- Full text of the webpage of junior roster in string format.
        The web page direction is similar at :
        /plantilla.php?juvenil=1&id_equipo=114
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
            avg = str(data_junior[3])[str(data_junior[3]).find('>')+1:str(data_junior[3]).find('</td>')]
            age = str(data_junior[5])[str(data_junior[5]).find('>')+1:str(data_junior[5]).find('</td>')]
            clause = str(data_junior[8])[str(data_junior[8]).find('right;">')+8:str(data_junior[8]).find('</td')-2]
            juniors.append(Junior(url,pos,avg,age,clause))
    return juniors

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