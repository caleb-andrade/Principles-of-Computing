"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans
    
    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods
    def __helper0__(self, string, ans):
        """
        performs a given set of movements given by string, updates answer
        """
        self.update_puzzle(string)
        #print self
        return ans + string
        
    def __helper1__(self, top, low, string, ans):
        """
        moves zero tile in the direction specified by string, repeatedly,
        updates answer
        """
        for dummy_i in range(top - low):
            ans = self.__helper0__(string, ans)
        return ans
    
    def __helper2__(self, string, ans, target_row, target_col, tar_tile):
        """
        moves target tile to its correct position (in cycles given by string)
        updates answer
        """
        while self.get_number(target_row, target_col) != tar_tile:
            ans = self.__helper0__(string, ans)
        return ans 
    
    def __helper3__(self, string, ans, target_row, target_col):
        """
        moves target tile to its target col, specified by string, updates answer
        """
        while self.current_position(target_row, target_col)[1] != target_col:
            ans = self.__helper0__(string, ans)
        return ans        
        
    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        height = self.get_height()
        width = self.get_width()
        if self.get_number(target_row, target_col) != 0:
            return False
            
        if target_row + 1 < height:
            for idx in range(target_row + 1, height):
                for jdx in range(width):
                    if self.get_number(idx, jdx) != idx*width + jdx:
                        return False
                    
        if target_col + 1 < width:
            for jdx in range(target_col + 1, width):
                if self.get_number(target_row, jdx) != target_row*width + jdx:
                    return False
        return True

    def solve_interior_tile(self, tar_row, tar_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string. Assume i > 1, j > 0
        """
        ans = ""
        temp = self.current_position(tar_row, tar_col)
        tar_tile = self.get_number(temp[0], temp[1])
               
        # case 1, target tile is in the same row and to the left of zero
        if tar_row == temp[0]:
            ans = self.__helper1__(tar_col, temp[1], 'l', ans)
            ans = self.__helper2__('urrdl', ans, tar_row, tar_col, tar_tile)
            return ans
        else: 
            # in this step the zero tile is elevated until row containing tar_tile
            ans = self.__helper1__(tar_row, temp[0], 'u', ans)
                           
        # case 3, above to the right
        if tar_col < temp[1]:
            ans = self.__helper1__(temp[1], tar_col, 'r', ans)
            if self.current_position(tar_row, tar_col)[0] == 0:
                char = 'dllur'
            else:
                char = 'ulldr'
            ans = self.__helper3__(char, ans, tar_row, tar_col)
            if self.current_position(tar_row, tar_col)[0] == 0:
                ans = self.__helper0__('dlu', ans)
            else:
                ans = self.__helper0__('ul', ans)
                        
        # case 4, above to the left
        if tar_col > temp[1]:
            ans = self.__helper1__(tar_col, temp[1], 'l', ans)
            ans = self.__helper3__('drrul', ans, tar_row, tar_col)
            ans = self.__helper0__('dru', ans)
                
        # case 2, target tile is above 
        if self.current_position(tar_row, tar_col)[1] == tar_col:
            ans = self.__helper2__('lddru', ans, tar_row, tar_col, tar_tile)
               
        ans = self.__helper0__('ld', ans)
        return ans
                
    def solve_col0_tile(self, tar_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        #print "-----------------INITIAL STATE-------------------- \n", self
        ans = self.__helper0__('ur', "")
        temp = self.current_position(tar_row, 0) # current position of tar_tile
        tar_tile = self.get_number(temp[0], temp[1])
        
        if temp[0] == tar_row and temp[1] == 0: # check if tar_tile is in place
            ans = self.__helper1__(self.get_width() - 2, 0, 'r', ans) # move it to rigthmost cell
            return ans
        
        if self.get_width() > 2:
            # if puzzle has width greater than 2, we will reduce it to the case 3x2
            ans = self.__helper1__(tar_row - 1, temp[0], 'u', ans) # move zero tile to tar_tile row
            #print "moved up"
            ans = self.__helper1__(temp[1], 1, 'r', ans)
            #print "moved to the right"
            if temp[0] == 0:
                char = 'dllur'
            else:
                char = 'ulldr'
            ans = self.__helper3__(char, ans, tar_row, 0)
            #print "next move completed"
            if temp[0] == tar_row - 1:
                ans = self.__helper0__('uldr', ans)
            elif temp[0] == tar_row - 2:
                ans = self.__helper0__('d', ans)
            else:
                ans = self.__helper1__(tar_row, 2 + temp[0], 'dlurd', ans)
                ans = self.__helper0__('d', ans)
            #print "almost there!"        
        
        while self.get_number(tar_row - 2, 0) != tar_tile:
            ans = self.__helper0__('uldr', ans)
        
        ans = self.__helper0__('dlurdluurddlu', ans)
        ans = self.__helper1__(self.get_width() - 1, 0, 'r', ans) # move it to rigthmost cell
        
        return ans

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        clone = self.clone()
        width = self.get_width()
        height = self.get_height()
        if clone.current_position(0, 0)[0] < height - 1:
            clone.update_puzzle('d')
        ans = clone.row1_invariant(target_col)
        return ans and self.get_number(1, target_col) == width + target_col
        
    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        ans = self.lower_row_invariant(1, target_col)
        width = self.get_width()
        if target_col + 1 < width:
            #print "lets check first row"
            for idx in range(target_col + 1, width):
                if self.get_number(0, idx) != idx:
                    #print "first row wrong!"
                    return False 
        return ans
            
    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        ans = ""
        #print "Initial state: \n", self
        if not self.row0_invariant(target_col):
            #print "does not meet row0_invariant!"
            return ans
        ans = self.__helper0__('l', ans)
        if self.get_number(0, target_col) == target_col:
            ans = self.__helper0__('d', ans)
            return ans
        elif self.get_number(0, target_col - 2) != target_col:
            while self.get_number(0, target_col - 2) != target_col:
                ans = self.__helper1__(target_col, 1, 'l', ans)
                ans = self.__helper0__('d', ans)
                ans = self.__helper1__(target_col, 1, 'r', ans)
                ans = self.__helper0__('u', ans)
        ans = self.__helper0__('rdluldrruld', ans)
        return ans
            
    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        ans = ""
        #print "Initial state: \n", self
        if not self.row1_invariant(target_col):
            #print "does not meet row1_invariant!"
            return ans
        
        while not self.row0_invariant(target_col):
            ans = self.__helper1__(target_col, 0, 'l', ans)
            ans = self.__helper0__('u', ans)
            ans = self.__helper1__(target_col, 0, 'r', ans)
            if self.row0_invariant(target_col):
                return ans
            else:
                ans = self.__helper0__('d', ans)
        return ans
            

    ###########################################################
    # Phase 3 methods
    
    def __helper4__(self):
        """
        checks that the 2x2 is solved
        """
        if self.get_number(0, 0) != 0:
            return False
        if self.get_number(0, 1) != 1:
            return False
        if self.get_number(1, 0) != self.get_width():
            return False
        if self.get_number(1, 1) != self.get_width() + 1:
            return False
        return True        
    
    def __helper5__(self, ans):
        """
        retrieves the position of zero tile in the 2x2 puzzle
        """
        pos = self.current_position(0, 0)
        if pos[0] == 0 and pos[1] == 0:
            return ans
        if pos[0] == 0 and pos[1] == 1:
            self.update_puzzle('l')
            return ans + 'l'
        if pos[0] == 1 and pos[1] == 0:
            self.update_puzzle('u')
            return ans + 'u'
        if pos[0] == 1 and pos[1] == 1:
            self.update_puzzle('ul')
            return ans + 'ul'
        
    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        #print "INITIAL STATE\n", self
        ans = self.__helper5__("")
        while not self.__helper4__():
            ans = self.__helper0__('d', ans)
            if self.__helper4__():
                return ans
            ans = self.__helper0__('r', ans)
            if self.__helper4__():
                return ans
            ans = self.__helper0__('u', ans)
            if self.__helper4__():
                return ans
            ans = self.__helper0__('l', ans)
            if self.__helper4__():
                return ans
        return ans
    
    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        ans = ""
        height = self.get_height()
        width = self.get_width()
        #print "Initial State: \n", self
        pos = self.current_position(0, 0)
        ans = self.__helper1__(width, pos[1] + 1, 'r', ans)
        ans = self.__helper1__(height, pos[0] + 1, 'd', ans)
        pos = self.current_position(0, 0)
        #print "Got to the corner!"
        while pos[0] > 1:
            if pos[1] == 0:
                #print "solve_col0_tile"
                ans += self.solve_col0_tile(pos[0])
            else:
                #print "solve_interior_tile"
                ans += self.solve_interior_tile(pos[0], pos[1])
            pos = self.current_position(0, 0)
        while pos[1] > 1:
            if pos[0] == 0:
                ans += self.solve_row0_tile(pos[1])
            else:
                ans += self.solve_row1_tile(pos[1])
            pos = self.current_position(0, 0)
        ans += self.solve_2x2()
        
        return ans
        
# Start interactive simulation
# poc_fifteen_gui.FifteenGUI(Puzzle(5, 5))

# TESTS
"""
x = Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [7, 0, 8]])
print x.lower_row_invariant(2, 1) # True
x = Puzzle(4, 5, [[12, 11, 10, 9, 8], [7, 6, 5, 4, 3], [2, 1, 0, 13, 14], [15, 16, 17, 18, 19]])
print x.lower_row_invariant(2, 2) # True
x = Puzzle(2, 2, [[0, 1], [2, 3]])
print x.lower_row_invariant(0, 0) # True
x = Puzzle(3, 3, [[1, 0, 2], [6, 5, 4], [7, 3, 8]])
print x.lower_row_invariant(0, 1) # False
x = Puzzle(3, 3, [[1, 3, 2], [6, 0, 5], [6, 7, 8]])
print x.lower_row_invariant(1, 1) # True
x = Puzzle(4, 5, [[12, 11, 10, 9, 8], [7, 6, 5, 4, 3], [13, 2, 1, 0, 14], [15, 16, 17, 18, 19]])
print x.lower_row_invariant(2, 3) # True

x = Puzzle(4, 5, [[12, 11, 3, 9, 8], [1, 6, 5, 4, 7], [10, 2, 0, 13, 14], [15, 16, 17, 18, 19]])
x.solve_interior_tile(2, 2)
x = Puzzle(4, 5, [[1, 11, 3, 9, 8], [12, 6, 5, 4, 7], [10, 2, 0, 13, 14], [15, 16, 17, 18, 19]])
x.solve_interior_tile(2, 2)
x = Puzzle(4, 5, [[6, 11, 3, 9, 8], [1, 12, 5, 4, 7], [10, 2, 0, 13, 14], [15, 16, 17, 18, 19]])
x.solve_interior_tile(2, 2)
x = Puzzle(4, 5, [[6, 12, 3, 9, 8], [1, 11, 5, 4, 7], [10, 2, 0, 13, 14], [15, 16, 17, 18, 19]])
x.solve_interior_tile(2, 2)
x = Puzzle(4, 5, [[8, 11, 3, 9, 12], [1, 6, 5, 4, 7], [10, 2, 0, 13, 14], [15, 16, 17, 18, 19]])
x.solve_interior_tile(2, 2)
x = Puzzle(4, 5, [[8, 11, 3, 12, 9], [1, 6, 5, 4, 7], [10, 2, 0, 13, 14], [15, 16, 17, 18, 19]])
x.solve_interior_tile(2, 2)
x = Puzzle(4, 5, [[8, 11, 3, 9, 7], [1, 6, 5, 4, 12], [10, 2, 0, 13, 14], [15, 16, 17, 18, 19]])
x.solve_interior_tile(2, 2)
x = Puzzle(4, 5, [[8, 11, 3, 9, 4], [1, 6, 5, 12, 7], [10, 2, 0, 13, 14], [15, 16, 17, 18, 19]])
x.solve_interior_tile(2, 2)
x = Puzzle(4, 5, [[8, 11, 3, 9, 10], [1, 6, 5, 4, 7], [12, 2, 0, 13, 14], [15, 16, 17, 18, 19]])
x.solve_interior_tile(2, 2)
x = Puzzle(4, 5, [[8, 11, 3, 9, 10], [1, 6, 5, 4, 7], [14, 2, 12, 13, 0], [15, 16, 17, 18, 19]])
x.solve_interior_tile(2, 4)
x = Puzzle(4, 5, [[8, 11, 3, 9, 10], [1, 6, 5, 4, 14], [7, 2, 12, 13, 0], [15, 16, 17, 18, 19]])
x.solve_interior_tile(2, 4)
x = Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [7, 0, 8]])
x.solve_interior_tile(2, 1)
x = Puzzle(4, 3, [[1, 6, 7], [4, 3, 5], [2, 0, 8], [9, 10, 11]])
x.solve_interior_tile(2, 1)
x = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])

x = Puzzle(3, 2, [[4, 2], [3, 1], [0, 5]])
x.solve_col0_tile(2)
x = Puzzle(4, 3, [[1, 2, 6], [4, 3, 5], [0, 7, 8], [9, 10, 11]])
x.solve_col0_tile(2)
x = Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [0, 7, 8]])
x.solve_col0_tile(2)
x = Puzzle(4, 5, [[2, 8, 3, 9, 10], [1, 6, 5, 4, 7], [0, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
x.solve_col0_tile(2)
x = Puzzle(4, 5, [[2, 8, 3, 9, 7], [1, 6, 5, 4, 10], [0, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
x.solve_col0_tile(2)
x = Puzzle(4, 5, [[12, 11, 10, 9, 15], [7, 6, 5, 4, 3], [2, 1, 8, 13, 14], [0, 16, 17, 18, 19]])
x.solve_col0_tile(3)

x = Puzzle(4, 4, [[4, 6, 1, 3], [5, 2, 0, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
print x
print x.row1_invariant(2)
print
x = Puzzle(4, 4, [[4, 6, 1, 3], [5, 2, 7, 0], [8, 9, 10, 11], [12, 13, 14, 15]])
print x
print x.row1_invariant(3)
print
x = Puzzle(4, 4, [[4, 6, 3, 1], [5, 2, 0, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
print x
print x.row1_invariant(2)
print
x = Puzzle(4, 4, [[4, 6, 1, 3], [5, 2, 7, 0], [9, 8, 10, 11], [12, 13, 14, 15]])
print x
print x.row1_invariant(3)
print
x = Puzzle(4, 4, [[4, 6, 1, 3], [5, 7, 0, 2], [8, 9, 10, 11], [12, 13, 14, 15]])
print x
print x.row1_invariant(2)
print

x = Puzzle(4, 4, [[4, 1, 0, 3], [5, 2, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
print x
print x.row0_invariant(2)
print
x = Puzzle(4, 4, [[4, 6, 1, 0], [5, 2, 3, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
print x
print x.row0_invariant(3)
print
x = Puzzle(4, 4, [[4, 3, 0, 1], [5, 2, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
print x
print x.row0_invariant(2)
print
x = Puzzle(4, 4, [[4, 6, 1, 0], [5, 2, 3, 7], [9, 8, 10, 11], [12, 13, 14, 15]])
print x
print x.row0_invariant(3)
print
x = Puzzle(4, 4, [[4, 1, 0, 3], [5, 7, 6, 2], [8, 9, 10, 11], [12, 13, 14, 15]])
print x
print x.row0_invariant(2)
print

x = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
print x
print x.row0_invariant(0)
print

x = Puzzle(4, 4, [[4, 6, 1, 3], [5, 2, 0, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
print x
print x.solve_row1_tile(2)
print
x = Puzzle(4, 4, [[4, 6, 1, 3], [5, 2, 7, 0], [8, 9, 10, 11], [12, 13, 14, 15]])
print x
print x.solve_row1_tile(3)
print
x = Puzzle(4, 4, [[4, 6, 3, 1], [5, 2, 0, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
print x
print x.solve_row1_tile(2)
print
x = Puzzle(4, 4, [[4, 6, 1, 3], [5, 2, 7, 0], [9, 8, 10, 11], [12, 13, 14, 15]])
print x
print x.solve_row1_tile(3)
print
x = Puzzle(4, 4, [[4, 6, 1, 3], [5, 7, 0, 2], [8, 9, 10, 11], [12, 13, 14, 15]])
print x
print x.solve_row1_tile(2)
print

x = Puzzle(3, 3, [[4, 1, 0], [2, 3, 5], [6, 7, 8]])
print x
print x.solve_row0_tile(2)
print x

x = Puzzle(4, 5, [[1, 2, 0, 3, 4], [6, 5, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
print x
print x.solve_row0_tile(2)
print x

x = Puzzle(2, 2, [[0, 1], [2, 3]])
x.solve_2x2()
print x
x = Puzzle(2, 2, [[1, 0], [2, 3]])
x.solve_2x2()
print x
x = Puzzle(2, 2, [[1, 3], [2, 0]])
x.solve_2x2()
print x
x = Puzzle(2, 2, [[1, 3], [0, 2]])
x.solve_2x2()
print x
x = Puzzle(2, 2, [[0, 3], [1, 2]])
x.solve_2x2()
print x
x = Puzzle(2, 2, [[3, 0], [1, 2]])
x.solve_2x2()
print x
x = Puzzle(2, 2, [[3, 2], [1, 0]])
x.solve_2x2()
print x
x = Puzzle(2, 2, [[3, 2], [0, 1]])
x.solve_2x2()
print x
x = Puzzle(2, 2, [[0, 2], [3, 1]])
x.solve_2x2()
print x
x = Puzzle(2, 2, [[2, 0], [3, 1]])
x.solve_2x2()
print x
x = Puzzle(2, 2, [[2, 1], [0, 3]])
x.solve_2x2()
print x
x = Puzzle(2, 2, [[2, 1], [3, 0]])
x.solve_2x2()
print x

x = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
x.solve_puzzle()
print x
x = Puzzle(3, 3, [[7, 1, 2], [3, 4, 5], [6, 0, 8]])
x.solve_puzzle()
print x
x = Puzzle(3, 3, [[4, 1, 2], [3, 5, 0], [6, 7, 8]])
x.solve_puzzle()
print x
x = Puzzle(3, 3, [[8, 7, 6], [5, 0, 3], [2, 1, 4]])
x.solve_puzzle()
print x
x = Puzzle(3, 3, [[3, 1, 2], [0, 4, 5], [6, 7, 8]])
x.solve_puzzle()
print x
x = Puzzle(3, 3, [[8, 7, 0], [5, 4, 3], [2, 6, 1]])
x.solve_puzzle()
print x
x = Puzzle(3, 3, [[4, 0, 2], [3, 1, 5], [6, 7, 8]])
x.solve_puzzle()
print x
x = Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
x.solve_puzzle()
print x
x = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
x.solve_puzzle()
print x
"""