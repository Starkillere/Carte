# -*- coding:utf-8 -*-

import csv

class MyStat(object):
    def __init__(self, filename:str) -> None:
        with open(filename, 'r', encoding='utf-8') as file:
            self.data = [dict(row) for row in csv.DictReader(file)]
        self.head = []
        if len(self.data) > 0:
            self.length = len(self.data)
            self.head = list(self.data[0].keys())
            self.lengthHead = len(self.head)
    
    def dict_smoll_stat(self):
        statDict =  {}
        if len(self.data) > 0:
            statDict["Nombre de vote"] = self.length
            for row in self.head:
                statDict[row] = (sum([int(elmt[row]) for elmt in self.data])/self.length)*100
                statDict[f"{row}_nombre"] = sum([int(elmt[row]) for elmt in self.data])
        return statDict
        