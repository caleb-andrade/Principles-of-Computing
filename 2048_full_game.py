"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    result = [0 for idx in range(len(line))]
    count = 0
    # push all non-zero values to the left of the tile
    for num in line:
        if num != 0:
            result[count] = num
            count += 1
    # merge adjacent values only once left to right
    for idx in range(len(list(result))-1):
        if result[idx] == result[idx+1]:
            result[idx] = result[idx] + result[idx+1]
            result.pop(idx+1)
            result.append(0)
    return result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.reset()
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self.grid = [[0 for col in range(self.grid_width)] for row in range(self.grid_height)]
        # next, create a list of all tuples (row,col)
        self.tiles = [(row,col) for row in range(self.grid_height) for col in range(self.grid_width)] 
        for dummy_idx in range(2):
            self.new_tile()
        self.dir_dic = {
            UP:[(0, col) for col in range(self.grid_width)],
            DOWN:[(self.grid_height-1, col) for col in range(self.grid_width)],
            LEFT:[(row,0) for row in range(self.grid_height)], 
            RIGHT:[(row,self.grid_width-1) for row in range(self.grid_height)]}
        
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        grid_str = ""
        for row in range(self.grid_height):
            grid_str += str(self.grid[row])+'\n'
        return grid_str

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        moved = False
        initial_tiles = self.dir_dic[direction]
        offset = OFFSETS[direction]
        if direction == UP or direction == DOWN:
            bound = self.grid_height
        else:
            bound = self.grid_width
        for tile in initial_tiles:
            temp = [self.get_tile(tile[0] + idx*offset[0], tile[1] + idx*offset[1]) 
                    for idx in range(bound)]
            temp = merge(temp)
            
            for idx in range(bound):
                row = tile[0] + idx*offset[0]
                col = tile[1] + idx*offset[1]
                if self.get_tile(row, col) != temp[idx]:
                    moved = True
                self.set_tile(row, col, temp[idx]) 
        if moved:
            self.new_tile()
    
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        random.shuffle(self.tiles) # shuffle the list of tiles tuples
        count = 0
        while self.get_tile(self.tiles[0][0], self.tiles[0][1]) != 0 and count < self.grid_height*self.grid_width: 
            self.tiles.append(self.tiles.pop(0))            
            
        # next, select value as 2 with a 90% probability (percentage) and 4 with 10%
        percentage = random.random() 
        if percentage > 0.1:
            value = 2
        else:
            value = 4
        row = self.tiles[0][0]
        col = self.tiles[0][1]
        self.set_tile(row , col,value) 

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        #print 'The value of tile at position: (',row,',',col,') is: ',self.grid[row][col]
        return self.grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))


