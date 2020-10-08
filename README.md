# SudokuPuzzle

Work in progress

Solves a Sudoku puzzle

Files included:
- Sudoku.py         -> Contains the SudokuSolver class that represents a Sudoku puzzle and contains the functions needed to solve it
- Box.py            -> Contains the Box class which represents one of the boxes making up the 9x9 grid on a Sudoku puzzle
- SudokuGUI.py      -> PyQT GUI for interacting with the SudokuSolver class. SudokuSolver can be used without this, but this is a nice way for a user to input a puzzle
- SudokuGUI.ui      -> UI file for QTDesigner that made SudokuGUI.py
- Book1.xlsx        -> Sample Sudoku puzzle 1
- Book2.xlsx        -> Sample Sudoku puzzle 2
- TestOutput.xlsx   -> Answer for the puzzle in Book1.xlsx

To use the Sudoku solver, two options are available:
- GUI Option
  - Run the SudokuGUI.py file to open the interface
  - Input the known values of the Sudoku puzzle you wish to solve in the appropriate places on the 9x9 grid given
  - Make sure the checkboxes for at least one of the solution methods is checked (I recommend always leaving analytical checked as brute force can take too long)
  - Click Solve
- Non-GUI Options
  - Store the Sudoku puzzle you wish to solve in an Excel .xlsx file with the known numbers placed in the appropriate location on the 9x9 grid and 0 everywhere else in the 9x9 grid
  - Create a SudokuSolver Object ( puzzle = SudokuSolver() )
  - Run the read_grid method and pass in the name of your .xlsx file containing the puzzle ( puzzle.read_grid( "my_sudoku.xlsx" ) )
  - Run the solve method ( puzzle.solve() ) where you may optionally set one of the solution methods to false

Currently works, at least for all cases I have tried, but the following needs to be done
- Rename all instances of SudokuSolver to SudokuPuzzle to be consistent with other similar projects of mine
- Implement more advanced functions in the analytical search so the brute force search happens less frequently, even with more advanced puzzles
