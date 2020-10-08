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

# Terminology used
# Row       - Row of boxes in a Sudoku grid
# Column    - Column of boxes in a Sudoku grid
# Sector    - 3x3 sub-grid in a Sudoku puzzle, 9 of these make up the whole grid

# Class that represents a Sudoku puzzle and all the functions required ot solve a puzzle
class SudokuSolver:
    def __init__(self):
        self.message = ""                                           # Message to print to the GUI, letting the user know the results
        self.grid = np.repeat(None, DIM*DIM).reshape((DIM,DIM))     # The grid of boxes representing the Sudoku squares
        # Initialize the grid
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
            
            # Initializes the grid with values from the file
            for row in range(s.nrows):
                for col in range(s.ncols):
                    self.grid[row,col] = Box()
                    self.grid[row,col].set_value(int(s.cell(row,col).value))
                    self.grid[row,col].x = col
                    self.grid[row,col].y = row
        self.reduce_grid()
    
    # Loads grid given an array of numbers
    # This function replaces read_grid when using the UI
    def load_grid(self, arr):
        for i in range(DIM):
            for j in range(DIM):
                self.grid[i,j] = Box()
                self.grid[i,j].set_value(int(arr[i,j]))
                self.grid[i,j].x = j
                self.grid[i,j].y = i
        self.reduce_grid()
    
    # Reduce possibilities in remaining boxes given the filled values
    def reduce_grid(self):
        for y in range(DIM):
            for x in range(DIM):
                if not self.grid[y,x].solved:
                    # Get all of the filled values in the same row, grid, or sector
                    # These will be removed from the possibilities of the current Box
                    vals = self.get_collisions(x,y)
                    
                    for num in vals:
                        if num in self.grid[y,x].possibilities:
                            self.grid[y,x].remove_possibility(num)
                    self.remove_possibilities(x,y)                  # Account for any newly set values in the grid
                    self.grid[y,x].check_possibilities()            # Check the current box to see if there's only one possibility
                    
        # Do a full sweep of the grid and update any possibilities in all the boxes
        for y in range(DIM):
            for x in range(DIM):
                self.remove_possibilities(x,y)
    
    # PART B #######################################################################################
    # TODO Implement more advanced parts of the analytical search, empty functions already included below
    # Solve the grid
    # algorithm         When True, attempt to solve the grid using the analytical method first
    # brute             When True, use the brute force approach (after analytical, if also set to True)
    def solve(self, algorithm=True, brute=True):
        begin = time.time()                             # Time the whole proces, you know, for fun
        changes = 1                                     # Keep track of the number of changes made each sweep
        
        #Analytical algorithm
        if algorithm:
            while changes > 0:
                changes = self.solve_analytical()
                #if changes == 0:
                #    print("Advanced")
                #    changes += self.advanced_solve()
        
        end_algorithm = time.time()                                                 # How long did the analytical method take?
        grid_value = sum([box.remaining for box in self.grid.reshape(DIM*DIM)])     # See how many unsolved boxes there are
        done = self.verify_completed()                                              # See if the puzzle has been solved
        
        #Brute force algorithm
        if brute:
            self.solve_brute(done, algorithm, grid_value)
        
        end_brute = time.time()                                                     # End of the whole solve method
        
        # Just some messages to display to the GUI to inform the user about how long the process took
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
    
    # The analytical method
    # Solves using logic and following a deterministic procedure
    def solve_analytical(self):
        changes = 0                                         # See if any changes are made
        
        # Try each of these three singleton methods, described later
        # In short, checks to see if there are any possibilities that only appear once in a row, column, or sector
        for ind in range(DIM):
            changes += self.singleton_column(ind)
        for ind in range(DIM):
            changes += self.singleton_row(ind)
        for y in range(SUB_DIM):
            for x in range(SUB_DIM):
                changes += self.singleton_sector(x,y)
        # Return the number of changes made
        return changes
    
    # Uses more advanced algorithms
    # TODO : Verify that this works (test on puzzles too hard for the current method to work)
    # TODO : Implement this
    # TODO : Include n_column, n_row, and n_sector, listed below
    def advanced_solve(self):
        changes = 0
        for y in range(SUB_DIM):
            for x in range(SUB_DIM):
                print((x,y))
                changes += self.force_row(x,y)
                changes += self.force_column(x,y)
        return changes
    
    # Function to brute force solve (in a somewhat intelligent manner)
    # On its own, this is unreasonable, but in cases where the analytical method can't do it entirely,
    # this is enough
    def solve_brute(self, done, algorithm, grid_value):
        # Check to see if we even need to attempt a brute force solution
        if done:
            print("Fully Solved Algorithmically")
            self.message += "Fully Solved Algorithmically\n"
        else:
            # If we attempted the algorithm first, give a message to alert the user that it wasn't enough
            if algorithm:
                print("Unable To Fully Solve Algorithmically, Brute Force Required")
                self.message += "Unable To Fully Solve Algorithmically, Brute Force Required\n"
            print("Remaining Boxes: ",grid_value)
            self.message += "Using Brute Force\n"
            self.message += "Remaining Boxes: " + str(grid_value) + "\n"
            self.brute_force()              # Actually call the brute_force method
    
    # Find any potential values (in the possibilities) in the current row that only appear once
    def singleton_row(self, ind):
        changes = 0
        
        frequencies = {}                                #Frequencies of the various possibilities
        for num in numbers:
            frequencies[num] = 0
        
        # Check all the boxes in the row specified at ind and check their possibilities
        for box in self.grid[ind,:]:
            # For each possibility in the current box, add one to its frequency count
            for pot in box.possibilities:
                frequencies[pot] += 1
        
        # Now check the counts for each potential value
        for key in frequencies:
            # Because each row needs exactly one of each number, if a number only appears as a possibility
            # in a single box, it must go there
            if frequencies[key] == 1:
                for box in self.grid[ind,:]:
                    if key in box.possibilities:
                        box.set_value(key)
                        self.remove_possibilities(box.x, box.y)             # Clean up and remove the set value from the possibilities of other boxes
                        changes += 1                                        # Add to the change count
                        break
        
        return changes
    
    # Find any potential values in the current column that only appear once
    def singleton_column(self, ind):
        changes = 0
        
        frequencies = {}            #Frequencies of the various possibilities
        for num in numbers:
            frequencies[num] = 0
        
        # Check all the boxes in the column specified at ind and check their possibilities
        for box in self.grid[:,ind]:
            # For each possibility in the current box, add one to its frequency count
            for pot in box.possibilities:
                frequencies[pot] += 1
        
        # Now check the counts for each potential value
        for key in frequencies:
            # Because each column needs exactly one of each number, if a number only appears as a possibility
            # in a single box, it must go there
            if frequencies[key] == 1:
                for box in self.grid[:,ind]:
                    if key in box.possibilities:
                        box.set_value(key)
                        self.remove_possibilities(box.x, box.y)             # Clean up and remove the set value from the possibilities of other boxes
                        changes += 1                                        # Add to the change count
                        break
        
        return changes
        
    # Find any potential values in the current sector that only appear once
    def singleton_sector(self, x, y):
        changes = 0
        
        frequencies = {}            #Frequencies of the various possibilities
        for num in numbers:
            frequencies[num] = 0
        
        # Check all the boxes in the sector specified at ind and check their possibilities
        for box in self.get_sector(x,y).reshape(DIM):
            # For each possibility in the current box, add one to its frequency count
            for pot in box.possibilities:
                frequencies[pot] += 1
        
        # Now check the counts for each potential value
        for key in frequencies:
            # Because each sector needs exactly one of each number, if a number only appears as a possibility
            # in a single box, it must go there
            if frequencies[key] == 1:
                for box in self.get_sector(x,y).reshape(DIM):
                    if key in box.possibilities:
                        box.set_value(key)
                        self.remove_possibilities(box.x, box.y)             # Clean up and remove the set value from the possibilities of other boxes
                        changes += 1                                        # Add to the change count
                        break
        
        return changes
    
    # If there there n boxes that share the same n possibilities, those n possibilities
    # cannot go in any other boxes in that row
    # e.g. if two boxes have possibilities 1,2 then all other 1 and two possibilities in that row
    # go away
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
    # TODO : Check these, make them work, implement
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
    
    # TODO : Check, fix, implement
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
    
    # Brute force any remaining empty boxes, somewhat intelligently
    def brute_force(self):
        # Get one remaining grid
        solution = self.test_solutions()
        if not solution is None:
            for i in range(DIM):
                for j in range(DIM):
                    self.grid[i,j].set_value(int(solution[i,j]))
    
    # Finds the potential arrangements of values within each row
    def get_potential_rows(self):
        pot_rows = []                       # A list of all potential lists of rows, the index in this list refers to a list of the potential rows for the row of the same index
        # e.g. pot_rows[0] holds a list for all possible row configurations of row 0
        # Iterate through each row
        for i in range(DIM):
            row = []
            # Go through all the boxes in the current row
            for box in self.grid[i,:]:
                # If the current box already has a value, we can't alter it, use it
                if box.solved:
                    if row == []:
                        # If there is nothing else in the row list, just append a list with the box's value in it
                        row.append([box.value])
                    else:
                        # Append the current value to every potential list
                        for path in row:
                            path.append(box.value)
                elif row == []:
                    # If the row potentials is just an empty list, add a list for every possibility remaining in the current box
                    # e.g. if the current box can be {1,2,3}, row goes from [] to [ [1], [2], [3] ]
                    # representing 3 new potential rows, starting with values 1, 2, and 3 respectively
                    for potential in box.possibilities:
                        row.append([potential])
                else:
                    new_list = []
                    # For each potential row that we currently have built
                    for path in row:
                        # To each potential row, create a copy and append one of the possibilities for each
                        # e.g. if the current possible rows are [ [1,2], [1,3] ] and the current box has the possibilities {5,7,8}
                        # the new possible rows are [ [1,2,5], [1,2,7], [1,2,8], [1,3,5], [1,3,7], [1,3,8] ]
                        for potential in box.possibilities:
                            # Don't add the possibility if it already exists in the possible row (though it shouldn't with the precautions taken)
                            if not potential in path:
                                temp = path.copy()
                                temp.append(potential)
                                new_list.append(temp)
                    row = new_list
            pot_rows.append(row)
        return pot_rows
    
    #Finds the potential combinations of rows to make a viable grid
    def get_potential_grids(self):
        # Get the list of all potential row arrangements for each row, given the known information
        all_rows = self.get_potential_rows()
        grids = []                              # A list of 2D arrays where each array is a possible Sudoku grid
        
        # Iterate through the potential rows
        # Each of these outer iterations will iterate through the lists of potential rows
        # e.g. the first loop, all_rows[0], accesses a list of all possible row configurations of row 0
        for i in range(len(all_rows)):
            if grids == []:
                # If grids is empty, then initialize as many grids as there are possibilities of first rows
                for row in all_rows[i]:
                    temp = np.zeros((DIM,DIM))          # Initialize grids
                    temp[i,:] = np.array(row)           # Set the first row to be one of the possible rows
                    grids.append(temp)                  # Add this grid to the possible grids
            else:
                new_grids = []                          # Placeholder because we will need to copy and alter every current grid in grids
                for grid in grids:
                    for row in all_rows[i]:
                        # For every possible configuration of the ith row, check if it is compatible with the current grid
                        if self.compatible(row,grid):
                            temp = np.copy(grid)                # Copy the current grid
                            temp[i,:] = np.array(row)           # set the ith row of this copy to the current row configuration
                            new_grids.append(temp)              # Add this new grid to the empty list of grids
                grids = new_grids                               # Replace grids with the updated new_grids
        
        print(len(grids)," Solutions Found")
        self.message += str(len(grids)) + " Solutions Found\n"
        return grids
    
    # Tries all of the solutions found by get_potential_grids to find one that works
    def test_solutions(self):
        tried = 0
        pot_grids = self.get_potential_grids()          # Get a list of all possible grid arrangements
        test_grid = SudokuSolver()                      # Create a Sudoku puzzle object to check each of these grids (These are filled grids, so we only need the verify functions)
        # Set the grid in the new SudokuSolver object to each of the potential grids and checks to see if it works
        for grid in pot_grids:
            for i in range(DIM):
                for j in range(DIM):
                    test_grid.grid[i,j].set_value(grid[i,j])
            tried += 1                                  # Count how many grids we have to check
            # If we found a grid that works, return it as the solution
            if test_grid.verify_completed():
                print("Tested ",tried," Solutions Before Finding Valid")
                self.message += "Tested " + str(tried) + " Solutions Before Finding Valid\n"
                return grid
        # Making it here means brute force couldn't find a solution
        print("No Valid Solution Found, Must Be Error In Code")
        self.message += "No Valid Solution Found\n"
        return None
    
    # PART C #######################################################################################
    # Checks to see that the grid is done
    def verify_completed(self):
        return self.verify_rows() and self.verify_cols() and self.verify_sectors()
    
    # Checks all the rows to make sure that each number appears exactly once in a given row
    def verify_rows(self, ind=0):
        # Because of the recursion, if we make it out of the array's dimensions, it is verified
        if ind >= DIM:
            return True
        
        valid = True
        vals = [b.value for b in self.grid[ind,:]]          # List of all the values in the current row
        for el in numbers:
            valid = valid and el in vals                    # Checks that each number appears exactly once
        
        # Recursive call, returns the validity of the and of the current row with the next row
        return valid and self.verify_rows(ind+1)
    
    # Same idea as verify_rows, checks that each number appears exactly once in a given column
    def verify_cols(self, ind=0):
        # Because of the recursion, if we make it out of the array's dimensions, it is verified
        if ind >= DIM:
            return True
        
        valid = True
        vals = [b.value for b in self.grid[:,ind]]          # List of all the values in the current column
        for el in numbers:
            valid = valid and el in vals                    # Checks that each number appears exactly once
        
        # Recursive call, returns the validity of the and of the current columns with the next column
        return valid and self.verify_cols(ind+1)
    
    # Same as verify_rows and verify_cols, checks that every number appears exactly once
    def verify_sectors(self, x=0, y=0):
        # Because of the recursive call, if we make it outside the dimensions of the array, it's verified
        if x >= SUB_DIM or y >= SUB_DIM:
            return True
        
        valid = True
        vals = [b.value for b in self.get_sector(x,y).reshape(DIM)]         # List of all the values in the current sector
        
        for el in numbers:
            valid = valid and el in vals                                    # Checks that each number appears exactly once
    
        # Recursive call, returns validity of the and of the current sector with the one below and the one to the right
        return valid and self.verify_sectors(x+1,y) and self.verify_sectors(x,y+1)
    
    # Misc - Helper functions ######################################################################
    
    # Sees if a particular row can be inserted into a grid without collision of elements
    # This limits the number of possibilities to check to just those that are valid
    def compatible(self, row, grid):
        for i in range(len(row)):
            # Check to see if any of the elements of the row clash with the elements in their respective column of the grid
            if row[i] in grid[:,i]:
                return False
        return True
    
    # Get the sector specified, dividing the Sudoku grid into a 2D array of indices [0:2, 0:2]
    # Returns the 3x3 sub-grid making up that sector
    def get_sector(self, x, y):
        return self.grid[SUB_DIM*y:SUB_DIM*y+SUB_DIM, SUB_DIM*x:SUB_DIM*x+SUB_DIM]
    
    # Given a location on the grid, return a set of all values in the same rows, column, and sector
    # to see what values cannot go in self.grid[y,x]
    def get_collisions(self, x, y):
        vals = set()
        [vals.add(b.value) for b in self.grid[y,:] ]
        [vals.add(b.value) for b in self.grid[:,x] ]
        [vals.add(b.value) for b in self.get_sector(int(x/SUB_DIM),int(y/SUB_DIM)).reshape(DIM)]

        if 0 in vals:
            vals.remove(0)
        
        return vals
    
    # Given a location on the grid that is solved, remove that value from all boxes in the same row, column, and sector
    def remove_possibilities(self, x, y):
        # If the current location is not solved, there's nothing to remove
        if not self.grid[y,x].solved:
            return
        
        val = self.grid[y,x].value
        
        # Remove the possibility from all boxes in the same row
        for box in self.grid[y,:]:
            # Only check those boxes that haven't been solved to avoid infinite recursion
            if not box.solved:
                box.remove_possibility(val)
                if box.solved:
                    # Recursive call, if removing the possibility solves a box, remove this new solution from the appropriate possibilities
                    self.remove_possibilities(box.x, box.y)
        
        # Remove the possibility from all boxes in the same column
        for box in self.grid[:,x]:
            # Only check those boxes that haven't been solved to avoid infinite recursion
            if not box.solved:
                box.remove_possibility(val)
                if box.solved:
                    # Recursive call, if removing the possibility solves a box, remove this new solution from the appropriate possibilities
                    self.remove_possibilities(box.x, box.y)
        
        # Remove the possibility from all boxes in the same sector
        for box in self.get_sector(int(x/SUB_DIM),int(y/SUB_DIM)).reshape(DIM):
            # Only check those boxes that haven't been solved to avoid infinite recursion
            if not box.solved:
                box.remove_possibility(val)
                if box.solved:
                    # Recursive call, if removing the possibility solves a box, remove this new solution from the appropriate possibilities
                    self.remove_possibilities(box.x, box.y)
    
    # Mostly administrative, print the current grid
    def print_grid(self):
        for i in range(DIM):
            row = []
            for j in range(DIM):
                row.append(self.grid[i,j].value)
            print(row)      