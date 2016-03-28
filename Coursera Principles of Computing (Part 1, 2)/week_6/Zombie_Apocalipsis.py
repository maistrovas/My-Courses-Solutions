"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import Grid_class as poc_grid
import Queue_Class as poc_queue
import poc_zombie_gui

# For OwlTest
# import random
# import poc_grid
# import poc_queue
# import poc_zombie_gui

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
        self._grid_height = grid_height
        self._grid_width = grid_width

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
        poc_grid.Grid.clear(self)
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
        return (zombi for zombi in self._zombie_list)
    
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
        return (person for person in self._human_list)
       
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        distance_field = [[self._grid_height * self._grid_width
                           for cell in range(self._grid_width)]
                          for cell in range(self._grid_height)]
        boundary = poc_queue.Queue()
        if entity_type == HUMAN:
            for elem in self._human_list:
                boundary.enqueue(elem)
        else:
            for elem in self._zombie_list:
                boundary.enqueue(elem)
        for cell in boundary:
            visited.set_full(cell[0], cell[1])
            distance_field[cell[0]][cell[1]] = 0
        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in neighbors:
                if visited.is_empty(neighbor[0], neighbor[
                        1]) and self.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighbor)
                    distance_field[neighbor[0]][neighbor[
                        1]] = distance_field[current_cell[0]][current_cell[1]] +1
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        if len(self._zombie_list) > 0:
            obstacle = self._grid_height * self._grid_width
            for index in range(len(self._human_list)):
                neighbors = self.eight_neighbors(self._human_list[index][0],
                                                 self._human_list[index][1])
                person_location_distance = zombie_distance_field[self._human_list[
                    index][0]][self._human_list[index][1]]
                #ways represented as [(100, (0, 8))]- dist, coordinate
                all_prosp_ways = [(zombie_distance_field[way[0]][way[1]], way) for way in neighbors
                                  if zombie_distance_field[way[0]][way[1]] != obstacle]
                all_prosp_ways.sort(reverse=True)
                best_way = all_prosp_ways[0][1]
                next_step_score = zombie_distance_field[best_way[0]][best_way[1]]
                if next_step_score != 0 and person_location_distance != 0:
                    self._human_list[index] = best_way
        else:
            pass
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        if len(self._human_list) > 0:
            obstacle = self._grid_height * self._grid_width
            for index in range(len(self._zombie_list)):
                neighbors = self.four_neighbors(self._zombie_list[index][0],
                                                self._zombie_list[index][1])
                zombie_location_distance = human_distance_field[self._zombie_list[index][
                    0]][self._zombie_list[index][1]]
                #ways represented as [(100, (0, 8))]- dist, coordinate
                all_prosp_ways = [(human_distance_field[way[0]][way[1]], way) for way in neighbors 
                                  if human_distance_field[way[0]][way[1]] != obstacle]
                if len(all_prosp_ways) > 0:
                    all_prosp_ways.sort()
                    best_way = all_prosp_ways[0][1]
                    if zombie_location_distance != 0:
                        self._zombie_list[index] = best_way
        else:
            pass
           
# Start up gui for simulation - You will need to write some code above
# before this will work without errors
poc_zombie_gui.run_gui(Apocalypse(30, 40))
#poc_zombie_gui.run_gui(Apocalypse(10, 10))
#poc_zombie_gui.run_gui(Apocalypse(3, 3, [(0, 1), (1, 2), (2, 1)], [(0, 2)], [(1, 1)]))
#poc_zombie_gui.run_gui(Apocalypse(3, 3, [(0, 0), (0, 1), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)], [(0, 2)], [(1, 1)]))


