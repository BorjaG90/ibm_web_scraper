# -*- coding: utf-8 -*-

__author__ = 'Borja Gete'
__email__ = 'borjagete90@outlook.es'

class Senior_Team:
    """Represent a line of the Senior roster, a player over 18."""

    def __init__(self, id_player, pos, power, ambition, loyalty, leadership, experience, speed, jump, resistance, level, level_points, pressure, rebound, block, steal, t2,t3,ft,assist,dribbling, dunk, fight, motivation):
        self._id = int(id_player)
        self.pos = pos
        self.power = int(power)
        self.ambition = int(ambition)
        self.loyalty = int(loyalty)
        self.leadership = int(leadership)
        self.experience = int(experience)
        self.speed = int(speed)
        self.jump = int(jump)
        self.resistance = int(resistance)
        self.level = int(level)
        self.level_points = int(level_points)
        self.pressure = int(pressure)
        self.rebound = int(rebound)
        self.block = int(block)
        self.steal = int(steal)
        self.t2 = int(t2)
        self.t3 = int(t3)
        self.ft = int(ft)
        self.assist = int(assist)
        self.dribbling = int(dribbling)
        self.dunk = int(dunk)
        self.fight = int(fight)
        self.motivation = int(motivation)

    def __str__(self):
        return "Id: {}, {} de {} años y {} de media,por {}€".format(
            self._id,
            self.position,
            self.average,
            self.clause
        )

    def to_db_collection(self):
        """Return the data of the senior in a legible MongoDB format."""
        position = self.pos.replace("SF","A").replace("PF","AP").replace("C","P").replace("PG","B").replace("SG","E")
        return {
            "_id":self._id,
        "pos":position,
        "power":self.power,
        "ambition":self.ambition,
        "loyalty":self.loyalty,
        "leadership":self.leadership,
        "experience":self.experience,
        "speed":self.speed,
        "jump":self.jump,
        "resistance":self.resistance,
        "level":self.level,
        "level_points":self.level_points,
        "pressure":self.pressure,
        "rebound":self.rebound,
        "block":self.block,
        "steal":self.steal,
        "t2":self.t2,
        "t3":self.t3,
        "ft":self.ft,
        "assist":self.assist,
        "dribbling":self.dribbling,
        "dunk":self.dunk,
        "fight":self.fight,
        "motivation":self.motivation
        }

class Junior_Team:
    """Represent a line of the junior roster, a player under 18."""

    def __init__(self, id_player, pos, power, ambition, loyalty, leadership, experience, speed, jump, resistance, level, level_points, pressure, rebound, block, steal, t2,t3,ft,assist,dribbling, dunk, fight):
        self._id = int(id_player)
        self.pos = pos
        self.power = int(power)
        self.ambition = int(ambition)
        self.loyalty = int(loyalty)
        self.leadership = int(leadership)
        self.experience = int(experience)
        self.speed = int(speed)
        self.jump = int(jump)
        self.resistance = int(resistance)
        self.level = int(level)
        self.level_points = int(level_points)
        self.pressure = int(pressure)
        self.rebound = int(rebound)
        self.block = int(block)
        self.steal = int(steal)
        self.t2 = int(t2)
        self.t3 = int(t3)
        self.ft = int(ft)
        self.assist = int(assist)
        self.dribbling = int(dribbling)
        self.dunk = int(dunk)
        self.fight = int(fight)

    def __str__(self):
        return "Id: {}, {} de {} años y {} de media,por €".format(
            self._id,
            self.position,
            self.average,
            self.clause
        )

    def to_db_collection(self):
        """Return the data of the senior in a legible MongoDB format."""
        position = self.pos.replace("SF","A").replace("PF","AP").replace("C","P").replace("PG","B").replace("SG","E")
        return {
            "_id":self._id,
        "pos":position,
        "power":self.power,
        "ambition":self.ambition,
        "loyalty":self.loyalty,
        "leadership":self.leadership,
        "experience":self.experience,
        "speed":self.speed,
        "jump":self.jump,
        "resistance":self.resistance,
        "level":self.level,
        "level_points":self.level_points,
        "pressure":self.pressure,
        "rebound":self.rebound,
        "block":self.block,
        "steal":self.steal,
        "t2":self.t2,
        "t3":self.t3,
        "ft":self.ft,
        "assist":self.assist,
        "dribbling":self.dribbling,
        "dunk":self.dunk,
        "fight":self.fight,
        "motivation":0
        }