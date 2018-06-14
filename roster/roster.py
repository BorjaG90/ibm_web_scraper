# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

class Junior:
    """Represent a line of the junior roster, a player under 18."""

    def __init__(self, id_player, pos, avg, age, clause):
        self._id = int(id_player)
        self.position = pos
        self.average = int(avg)
        self.age = int(age)
        self.clause = int(clause.replace('.',''))

    def __str__(self):
        return "Id: {}, {} de {} años y {} de media,por {}€".format(
            self._id,
            self.position,
            self.age,
            self.average,
            self.clause
        )

    def to_db_collection(self):
        """Return the data of the juior in a legible MongoDB format."""
        return {
            "_id":self._id,
            "position":self.position,
            "age":self.age,
            "average":self.average,
            "clause":self.clause
        }
