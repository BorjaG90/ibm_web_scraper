# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

from statistics.statistics import *

import re
import datetime

reg_day = '(Lunes|Martes|Miércoles|Jueves|Viernes|Sábado|Domingo),'
reg_hour = '(([01]\d|2[0-3]):([0-5]\d)|24:00)'

def analyze_game(html_str):
    """Analyze the html page of a Game.
    
    Return an array of statistics

    Keyword arguments:
    html_str -- Full text of the webpage of the game in string format.
        The web page direction is similar at :
        /partido.php?id=23656170&accion=alineaciones
    """
    url_visitor = html_str[html_str.find('nombreequipo2">')+15:]
    url_visitor = url_visitor[url_visitor.find('equipo.php?id=')+14:url_visitor.find('">')]
    url_home = html_str[html_str.find('nombreequipo1">')+15:]
    url_home = team_home_str[url_home.find('equipo.php?id=')+14:url_home.find('">')]
    type_game = html_str[html_str.find('<div id="fechapart"><span class="verde3">')+41:html_str.find('</span>')]

    print("Partido de {}, {} vs {}".format(type_game,url_home,url_visitor))
