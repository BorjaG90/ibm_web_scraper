# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

import transaction

def analyze_similar_buys(html_str):
    table_str = html_str[html_str.find('<tbody class="pijama">')+22:html_str.find('</tbody>')-8]
    players = table_str.replace('\n','').replace('\t','').split('<tr')
    transactions = []
    for player_str in players[1:]:
        data_player = player_str.split('<td')
        
        url = data_player[1][data_player[1].find('href="')+6:data_player[1].find('">')]
        #print(url)
        id_player = url[url.find('?id_jugador=')+12:] 
        name = data_player[1][data_player[1].find('">')+2:data_player[1].find('</a>')]
        date_buy = data_player[2][data_player[2].find('none;">')+7:data_player[2].find('</div>')]
        age = data_player[3][data_player[3].find('">')+2:data_player[3].find('</td>')]
        avg = data_player[4][data_player[4].find('">')+2:data_player[4].find('</td>')]
        pos = data_player[5][data_player[5].find('">')+2:data_player[5].find('</td>')]
        salary = data_player[6][data_player[6].find('">')+2:data_player[6].find('&euro;')]
        price = data_player[7][data_player[7].find('">')+2:data_player[7].find('&euro;')]
        type_buy = data_player[8][data_player[8].find('">')+2:data_player[8].find('</td>')]

        #print('Id: '+ id_player + ' Jugador: ' + name+ ' ' + pos +  ' de ' + age + ' años, con ' + avg + ' de media')
        #print('Vendido en ' + type_buy + ' por ' + price + '€, cobrando ' + salary + '€ en la fecha '+ date_buy +'\n')

        transactions.append(transaction.Transaction(id_player,date_buy,age,avg,pos,price,type_buy,salary))
    return transactions
#Main

path = input("Introduce la ruta del fichero html: ")
fichero = open(path,'r', encoding="utf8")

html_str = fichero.read()
ts = analyze_similar_buys(html_str)
for t in ts:
    print(t)

fichero.close