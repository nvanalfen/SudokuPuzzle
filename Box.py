# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 01:30:57 2018

@author: nvana
"""

# Class used to represent a single box on a Sudoku grid that holds one number
class Box:
    def __init__(self):
        self.solved = False
        self.value = 0
        self.remaining = 1
        self.possibilities = set((1,2,3,4,5,6,7,8,9))
        self.x = -1
        self.y = -1
    
    # Sets the value in a box, marks it as solved, and clears the possibilities
    def set_value(self, value):
        self.value = value
        self.temporary = value
        if value >= 1 and value <= 9:
            self.solved = True
            self.remaining = 0
            self.possibilities = set()
    
    # Removes a possibility from the set of possibilities
    # If only one possibility remains, set the value
    def remove_possibility(self, value):
        try:
            self.possibilities.remove(value)
            self.check_possibilities()
        except:
            pass
    
    # Checks the possibilities and if only one remains, set the value
    def check_possibilities(self):
        if len(self.possibilities) == 1:
            self.set_value(self.possibilities.pop())