# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

class Auction:
    """Represent a line of the market, a player in auction."""

    def __init__(self, id_player, pos, avg, age, date_auction, offer):
        self._id = int(id_player)
        self.position = pos
        self.average = int(avg)
        self.age = int(age)
        self.date_auction = date_auction
        self.offer = int(offer.replace('.',''))

    def __str__(self):
        return "Id: {}, {} de {} años y {} de media, hasta el {} por {}€".format(
            self._id,
            self.position,
            self.age,
            self.average,
            self.date_auction,
            self.offer
        )

    def to_db_collection(self):
        """Return the data of the auction in a legible MongoDB format."""
        position = self.position.replace("SF","A").replace("PF","AP").replace("C","P").replace("PG","B").replace("SG","E")
        return {
            "_id":self._id,
            "position":position,
            "age":self.age,
            "average":self.average,
            "date_acution":self.date_auction,
            "offer":self.offer
        }

    def pos_treatment(position):
        return position.replace("SF","A").replace("PF","AP").replace("C","P").replace("PG","B").replace("SG","E")