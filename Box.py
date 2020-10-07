# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 01:30:57 2018

@author: nvana
"""

class Box:
    def __init__(self):
        self.solved = False
        self.value = 0
        self.remaining = 1
        self.possibilities = set((1,2,3,4,5,6,7,8,9))
        self.x = -1
        self.y = -1
    
    def setValue(self, value):
        self.value = value
        self.temporary = value
        if value >= 1 and value <= 9:
            self.solved = True
            self.remaining = 0
            self.possibilities = set()
    
    def setSector(self, sector):
        self.sector = sector
    
    def removePossibility(self, value):
        try:
            self.possibilities.remove(value)
            self.checkPossibilities()
        except:
            pass
    
    def checkPossibilities(self):
        if len(self.possibilities) == 1:
            self.setValue(self.possibilities.pop())