"""
The 2048 game.
"""

import GUI_2048 as poc_2048_gui

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
    Helper function that merges a single row or column in 2048
    """
    zeros = []
    for _ in line:
        zeros.append(0)
    result_index = 0
    #in this step restlt = [0,0,0,0]
    result = zeros[:]
    for _ in range(len(line)):
        if line[_] != 0:
            result[result_index] = line[_]
            result_index +=1
    #in this step result = [2,2,2,0]
    for _ in range(1, len(result)):
        if result[_-1] ==result[_]:
            result[_-1] += result[_]
            result[_] = 0
    #in this step result = [4,0,2,0]
    final_result = zeros
    final_result_index = 0
    for _ in range(len(result[:])):
        if result[_] != 0:
            final_result[final_result_index] = result[_]
            final_result_index +=1
    return final_result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._up_initials = [(0, col) for col in range(grid_width)]
        self._down_initials = [(grid_height - 1, col) for col in range(grid_width)]
        self._left_initials = [(row, 0) for row in range(grid_height)]
        self._right_initials = [(row, grid_width - 1) for row in range(grid_height)]
        self._directions = {UP : self._up_initials, DOWN : self._down_initials,
                    LEFT : self._left_initials, RIGHT : self._right_initials}
        self._grid = []
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for dummy_col in range(self._grid_width)]
                                for dummy_row in range(self._grid_height)] 
        
        self.new_tile()
        self.new_tile()
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        for row in range(self._grid_height):
            grid = '{0}'.format(self._grid[row])
            print grid
        return ''

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """

        if direction == UP or direction == DOWN:
            num_steps = self._grid_height
        else:
            num_steps = self._grid_width
        change_counter = 0
        for start_cell in self._directions[direction]:
            merged_list = []
            for step in range(num_steps):
                row = start_cell[0] + step * OFFSETS[direction][0]
                col = start_cell[1] + step * OFFSETS[direction][1]
                merged_list.append(self._grid[row][col])
            
            for step in range(num_steps):
                moved_row = start_cell[0] + step * OFFSETS[direction][0]
                moved_col = start_cell[1] + step * OFFSETS[direction][1]
                self._grid[moved_row][moved_col] = merge(merged_list)[step]
            if merged_list == merge(merged_list):
                change_counter += 1
        if change_counter != num_steps:
            self.new_tile()
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        import random
        insertion = random.choice([2,2,2,2,2,2,2,2,2,4])
        empty_square = []
        while empty_square != 0:
            random_row = random.choice(range(self._grid_height))
            random_col = random.choice(range(self._grid_width))
            empty_square = self._grid[:][random_row][random_col]
        #Trial to make Lose Logic(no infiniti loop)
            empty_rows = 0
            for row in self._grid:
                if 0 not in row:
                    empty_rows +=1
            if empty_rows == (len(self._grid)):
                break
        if empty_rows != (len(self._grid)):
            self._grid[random_row][random_col] = insertion

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
