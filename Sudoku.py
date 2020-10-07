# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 01:20:59 2018

@author: nvana
"""

import numpy as np
import os
from xlrd import open_workbook
import time
from Box import Box

numbers = [1,2,3,4,5,6,7,8,9]
DIM = 9
SUB_DIM = 3

# PART A - Read in a Grid
# PART B - Solve grid
# PART C - Verify grid has been solved

class SudokuSolver:
    def __init__(self):
        self.message = ""
        self.grid = np.repeat(None, DIM*DIM).reshape((DIM,DIM))
        for i in range(DIM):
            for j in range(DIM):
                self.grid[i,j] = Box()
                self.grid[i,j].x = j
                self.grid[i,j].y = i
    
    # PART A #######################################################################################
    # Loads Sudoku grid from excel file
    def read_grid(self, f_name="Book1.xlsx"):
        if(os.path.isfile(f_name)):
            wb = open_workbook(f_name)
            s = wb.sheets()[0]
            
            for row in range(s.nrows):
                for col in range(s.ncols):
                    self.grid[row,col] = Box()
                    self.grid[row,col].set_value(int(s.cell(row,col).value))
                    self.grid[row,col].x = col
                    self.grid[row,col].y = row
        
        self.reduce_grid()
    
    #Loads grid given an array of numbers
    def load_grid(self, arr):
        for i in range(DIM):
            for j in range(DIM):
                self.grid[i,j] = Box()
                self.grid[i,j].set_value(int(arr[i,j]))
                self.grid[i,j].x = j
                self.grid[i,j].y = i
        self.reduce_grid()
    
    # Reduce possibilities in remaining boxes
    def reduce_grid(self):
        for y in range(DIM):
            for x in range(DIM):
                if not self.grid[y,x].solved:
                    
                    vals = self.get_collisions(x,y)
                    
                    for num in vals:
                        if num in self.grid[y,x].possibilities:
                            self.grid[y,x].remove_possibility(num)
                    self.remove_possibilities(x,y)
                    self.grid[y,x].check_possibilities()
                    
        for y in range(DIM):
            for x in range(DIM):
                self.remove_possibilities(x,y)
    
    # PART B #######################################################################################
    # TODO Implement more advanced parts of the analytical search, empty functions already included below
    def solve(self, algorithm=True, brute=True):
        begin = time.time()
        changes = 1
        
        #Analytical algorithm
        if algorithm:
            while changes > 0:
                #print("General")
                changes = self.solve_analytical()
                #if changes == 0:
                #    print("Advanced")
                #    changes += self.advanced_solve()
        
        end_algorithm = time.time()
        grid_value = sum([box.remaining for box in self.grid.reshape(DIM*DIM)])
        done = self.verify_completed()
        
        #Brute force algorithm
        if brute:
            self.solve_brute(done, algorithm, grid_value)
        
        end_brute = time.time()
        
        if algorithm and brute:
            self.message += "Algorithm Finished In " + str(end_algorithm-begin) + " Seconds\n"
            if not done:
                self.message += "Brute Force Finished In " + str(end_brute-end_algorithm) + " Seconds\n"
            self.message += "Total Time: " + str(end_brute-begin) + " Seconds\n"
        elif algorithm or brute:
            self.message += "Total Time: " + str(end_brute-begin) + " Seconds\n"
        else:
            self.message += "It's Really Hard To Solve A Sudoku Puzzle When You Tell Me Not To Solve It\n"
            self.message += "Choose At Least One Algorithm Type And Run Again...\n"
            self.message += "Moron...\n"
        
        return self.message
    
    def solve_analytical(self):
        changes = 0
        
        for ind in range(DIM):
            changes += self.singleton_column(ind)
        for ind in range(DIM):
            changes += self.singleton_row(ind)
        for y in range(SUB_DIM):
            for x in range(SUB_DIM):
                changes += self.singleton_sector(x,y)
        return changes
    
    #Uses more advanced algorithms
    def advanced_solve(self):
        changes = 0
        for y in range(SUB_DIM):
            for x in range(SUB_DIM):
                print((x,y))
                changes += self.force_row(x,y)
                changes += self.force_column(x,y)
        return changes
    
    def solve_brute(self, done, algorithm, grid_value):
        if done:
            print("Fully Solved Algorithmically")
            self.message += "Fully Solved Algorithmically\n"
        else:
            if algorithm:
                print("Unable To Fully Solve Algorithmically, Brute Force Required")
                self.message += "Unable To Fully Solve Algorithmically, Brute Force Required\n"
            print("Remaining Boxes: ",grid_value)
            self.message += "Using Brute Force\n"
            self.message += "Remaining Boxes: " + str(grid_value) + "\n"
            self.brute_force()
    
    # Find any potential values in the current row that only appear once
    def singleton_row(self, ind):
        changes = 0
        
        frequencies = {}            #Frequencies of the various possibilities
        for num in numbers:
            frequencies[num] = 0
        
        for box in self.grid[ind,:]:
            for pot in box.possibilities:
                frequencies[pot] += 1
        
        for key in frequencies:
            if frequencies[key] == 1:
                for box in self.grid[ind,:]:
                    if key in box.possibilities:
                        box.set_value(key)
                        self.remove_possibilities(box.x, box.y)
                        changes += 1
                        break
        
        return changes
    
    # Find any potential values in the current column that only appear once
    def singleton_column(self, ind):
        changes = 0
        
        frequencies = {}            #Frequencies of the various possibilities
        for num in numbers:
            frequencies[num] = 0
        
        for box in self.grid[:,ind]:
            for pot in box.possibilities:
                frequencies[pot] += 1
        
        for key in frequencies:
            if frequencies[key] == 1:
                for box in self.grid[:,ind]:
                    if key in box.possibilities:
                        box.set_value(key)
                        self.remove_possibilities(box.x, box.y)
                        changes += 1
                        break
        
        return changes
        
    # Find any potential values in the current sector that only appear once
    def singleton_sector(self, x, y):
        changes = 0
        
        frequencies = {}            #Frequencies of the various possibilities
        for num in numbers:
            frequencies[num] = 0
        
        for box in self.get_sector(x,y).reshape(DIM):
            for pot in box.possibilities:
                frequencies[pot] += 1
        
        for key in frequencies:
            if frequencies[key] == 1:
                for box in self.get_sector(x,y).reshape(DIM):
                    if key in box.possibilities:
                        box.set_value(key)
                        self.remove_possibilities(box.x, box.y)
                        changes += 1
                        break
        
        return changes
    
    #If there there n boxes that share the same n possibilities, those n possibilities
    #cannot go in any other boxes in that row
    #e.g. if two boxes have possibilities 1,2 then all other 1 and two possibilities in that row
    #go away
    def n_row(self):
        # TODO implement
        pass
    
    def n_column(self):
        # TODO Implement
        pass
    
    def n_sector(self):
        # TODO implement
        pass
    
    # If a value only takes up one row in a certain sector, eliminate those possibilities from the row
    # in other sectors
    def force_row(self, x, y):
        changes = 0
        
        rows = {}            #Frequencies of the various possibilities
        for num in numbers:
            rows[num] = set()
        
        #Fills the set for each value with all of the rows it can be in
        for box in self.get_sector(x,y).reshape(DIM):
            for pot in box.possibilities:
                rows[pot].add(box.y)
        
        #If any of the values only have one possible row, eliminate other values
        for key in rows:
            if len(rows[key]) == 1:
                row = rows[key].pop()
                for box in self.grid[row,0:x*3]:
                    if key in box.possibilities:
                        changes += 1
                        box.remove_possibility(key)
                for box in self.grid[row,(x*3)+3:]:
                    if key in box.possibilities:
                        changes += 1
                        box.remove_possibility(key)
        return changes
    
    def force_column(self, x, y):
        changes = 0
        
        cols = {}            #Frequencies of the various possibilities
        for num in numbers:
            cols[num] = set()
        
        #Fills the set for each value with all of the rows it can be in
        for box in self.get_sector(x,y).reshape(DIM):
            for pot in box.possibilities:
                cols[pot].add(box.x)
        
        #If any of the values only have one possible row, eliminate other values
        for key in cols:
            if len(cols[key]) == 1:
                changes += 1
                col = cols[key].pop()
                for box in self.grid[0:y*3,col]:
                    box.remove_possibility(key)
                for box in self.grid[(y*3)+3:,col]:
                    box.remove_possibility(key)
        return changes
    
    # Brute force any remaining empty boxes
    def brute_force(self):
        solution = self.test_solutions()
        if not solution is None:
            for i in range(DIM):
                for j in range(DIM):
                    self.grid[i,j].set_value(int(solution[i,j]))
    
    #Finds the potential arrangements of values within each row
    def get_potential_rows(self):
        pot_rows = []
        for i in range(DIM):
            row = []
            for box in self.grid[i,:]:
                if box.solved:
                    if row == []:
                        row.append([box.value])
                    else:
                        for path in row:
                            path.append(box.value)
                elif row == []:
                    for potential in box.possibilities:
                        row.append([potential])
                else:
                    new_list = []
                    for path in row:
                        for potential in box.possibilities:
                            if not potential in path:
                                temp = path.copy()
                                temp.append(potential)
                                new_list.append(temp)
                    row = new_list
            pot_rows.append(row)
        return pot_rows
    
    #Finds the potential combinations of rows to make a viable grid
    def get_potential_grids(self):
        all_rows = self.get_potential_rows()
        grids = []
        
        for i in range(len(all_rows)):
            if grids == []:
                for row in all_rows[i]:
                    temp = np.zeros((DIM,DIM))
                    temp[i,:] = np.array(row)
                    grids.append(temp)
            else:
                new_grids = []
                for grid in grids:
                    for row in all_rows[i]:
                        if self.compatible(row,grid):
                            temp = np.copy(grid)
                            temp[i,:] = np.array(row)
                            new_grids.append(temp)
                grids = new_grids
        
        print(len(grids)," Solutions Found")
        self.message += str(len(grids)) + " Solutions Found\n"
        return grids
    
    #Tries all ofthe solutions found by get_potential_grids to find one that works
    def test_solutions(self):
        tried = 0
        pot_grids = self.get_potential_grids()
        test_grid = SudokuSolver()
        for grid in pot_grids:
            for i in range(DIM):
                for j in range(DIM):
                    test_grid.grid[i,j].set_value(grid[i,j])
            tried += 1
            if test_grid.verify_completed():
                print("Tested ",tried," Solutions Before Finding Valid")
                self.message += "Tested " + str(tried) + " Solutions Before Finding Valid\n"
                return grid
        print("No Valid Solution Found, Must Be Error In Code")
        self.message += "No Valid Solution Found\n"
        return None
    
    # PART C #######################################################################################
    # Checks to see that the grid is done
    def verify_completed(self):
        return self.verify_rows() and self.verify_cols() and self.verify_sectors()
    
    def verify_rows(self, ind=0):
        if ind >= DIM:
            return True
        
        valid = True
        vals = [b.value for b in self.grid[ind,:]]
        for el in numbers:
            valid = valid and el in vals
        return valid and self.verify_rows(ind+1)
    
    def verify_cols(self, ind=0):
        if ind >= DIM:
            return True
        
        valid = True
        vals = [b.value for b in self.grid[:,ind]]
        for el in numbers:
            valid = valid and el in vals
        return valid and self.verify_cols(ind+1)
    
    def verify_sectors(self, x=0, y=0):
        if x >= SUB_DIM or y >= SUB_DIM:
            return True
        
        valid = True
        vals = [b.value for b in self.get_sector(x,y).reshape(DIM)]
        
        for el in numbers:
            valid = valid and el in vals
    
        return valid and self.verify_sectors(x+1,y) and self.verify_sectors(x,y+1)
    
    # Misc - Helper functions ######################################################################
    
    #Sees if a particular row can be inserted into a grid without collision of elements
    def compatible(self, row, grid):
        for i in range(len(row)):
            if row[i] in grid[:,i]:
                return False
        return True
    
    def get_sector(self, x, y):
        return self.grid[SUB_DIM*y:SUB_DIM*y+SUB_DIM, SUB_DIM*x:SUB_DIM*x+SUB_DIM]
    
    def get_collisions(self, x, y):
        vals = set()
        [vals.add(b.value) for b in self.grid[y,:] ]
        [vals.add(b.value) for b in self.grid[:,x] ]
        [vals.add(b.value) for b in self.get_sector(int(x/SUB_DIM),int(y/SUB_DIM)).reshape(DIM)]

        if 0 in vals:
            vals.remove(0)
        
        return vals
    
    def remove_possibilities(self, x, y):
        val = self.grid[y,x].value
        
        for box in self.grid[y,:]:
            if not box.solved:
                box.remove_possibility(val)
                if box.solved:
                    self.remove_possibilities(box.x, box.y)
            
        for box in self.grid[:,x]:
            if not box.solved:
                box.remove_possibility(val)
                if box.solved:
                    self.remove_possibilities(box.x, box.y)
        
        for box in self.get_sector(int(x/SUB_DIM),int(y/SUB_DIM)).reshape(DIM):
            if not box.solved:
                box.remove_possibility(val)
                if box.solved:
                    self.remove_possibilities(box.x, box.y)
    
    def print_grid(self):
        for i in range(DIM):
            row = []
            for j in range(DIM):
                row.append(self.grid[i,j].value)
            print(row)      