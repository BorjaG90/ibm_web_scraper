# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

class Transaction:

    def __init__(self,id_player,id_date_buy,age,avg,pos,price,type_buy,salary=None,date_buy=None):
        self._id_player = id_player
        self._id_date_buy = id_date_buy
        self.age = age
        self.average = avg
        self.position = pos
        self.price = price
        self.salary = salary
        self.type_buy = type_buy
        self.date_buy = date_buy

    def __str__(self):
        return 'Id: {} {} de {} años, con {} de media\nVendido en {} por {}€, cobrando {}€ en la fecha {}'.format(
            self._id_player
            , self.position
            , self.age
            , self.average
            , self.type_buy
            , self.price
            , self.salary
            , self._id_date_buy
        )

    def to_db_collection(self):
        return {
            "_id_player": self._id_player,
            "_id_date_buy": self._id_date_buy,
            "age": self.age,
            "average": self.average,
            "position": self.position,
            "price": self.price,
            "salary": self.salary,
            "type_buy": self.type_buy,
            "date_buy": self.date_buy
        }

    
