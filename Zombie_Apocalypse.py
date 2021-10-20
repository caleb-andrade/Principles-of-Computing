"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self) # inherits method from Grid class
        self._zombie_list = []
        self._human_list = []
        
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)     
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        hei = self.get_grid_height()
        wid = self.get_grid_width()
        visited = poc_grid.Grid(hei, wid)
        distance_field = [[hei*wid for dummy_i in range(wid)] for dummy_j in range(hei)]
        boundary = poc_queue.Queue()
        
        # Define whether we will calculate distance field for zombie or human
        if entity_type == ZOMBIE:
            copy_list = self._zombie_list
        else:
            copy_list = self._human_list
        
        for item in copy_list:
            boundary.enqueue(item) # create the "boundary" with entities
            visited.set_full(item[0], item[1]) # cells occupied by an entity marked as visited
            distance_field[item[0]][item[1]] = 0 # entity's distance cell initialized to zero
        
        # BFS algorithm
        while len(boundary) > 0:
            cell = boundary.dequeue()
            neighbors = visited.four_neighbors(cell[0], cell[1]) # cells to explore to calc. dist.
            for nei in neighbors:
                # if distance has not been calculated yet nor there is an obstacle...
                if visited.is_empty(nei[0], nei[1]) and self.is_empty(nei[0], nei[1]):
                    visited.set_full(nei[0], nei[1])
                    boundary.enqueue(nei)
                    distance_field[nei[0]][nei[1]] = distance_field[cell[0]][cell[1]] + 1
        
        return distance_field
    
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        human_temp = []
        zdf = zombie_distance_field
        for human in self._human_list:
            neighbors = self.eight_neighbors(human[0], human[1])
            best = human
            for neighbor in neighbors:
                row = neighbor[0]
                col = neighbor[1]
                if self.is_empty(row, col) and zdf[row][col] >= zdf[best[0]][best[1]]:
                    best = neighbor
            human_temp.append(best)
        self._human_list = human_temp
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        zombie_temp = []
        hdf = human_distance_field
        for zombie in self._zombie_list:
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            best = zombie
            for neighbor in neighbors:
                row = neighbor[0]
                col = neighbor[1]
                if self.is_empty(row, col) and hdf[row][col] <= hdf[best[0]][best[1]]:
                    best = neighbor
            zombie_temp.append(best)
        self._zombie_list = zombie_temp

# Start up gui for simulation - You will need to write some code above
# before this will work without errors
poc_zombie_gui.run_gui(Apocalypse(20, 20))