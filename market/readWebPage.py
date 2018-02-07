# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

def analyze_webpage(html_str):
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
        print("****\n")
        print(data_player[3])
        #for dat in data_player:
        #    print("\n" + dat)
        url = data_player[2][data_player[2].find('&id_jugador=')+12:data_player[2].find('" >')]
        pos = data_player[3][data_player[3].find('</div>')+6:data_player[3].find('</td>')]
        print(pos)

#Main
path = input("Introduce la ruta del fichero html: ")
fichero = open(path,'r', encoding="utf8")

html_str = fichero.read()
analyze_webpage(html_str)