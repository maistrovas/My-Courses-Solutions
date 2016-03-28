"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
-Implementation has refactoring issues.
-Overall Owl-Test score 92/100.
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

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        conditions = 0
        curent = self._grid[target_row][target_col] == 0
        if curent:
            conditions +=1
        else:
            print 'Tile ZERO is not at current position'
            return False

        last_row_ind = self._height - 1
        if target_row != last_row_ind:
            lower_row = target_row + 1
            for ind in range(len(self._grid[lower_row])):
                if self.current_position(lower_row, ind) != (lower_row, ind):
                    print 'Some tile in the lower row does not in correct place' 
                    return False
        conditions += 1
        # print len(self._grid[target_row])
        # print self._grid[target_row]
        # print self._grid[target_row][target_col+1:]
        right_part = self._grid[target_row][target_col+1:]
        
        for tile in range(1,len(right_part)+1):
            # print right_part.index(self._grid[target_col+1])
            # print tile
            # print self.current_position(target_row, target_col + tile)
            # print (target_row, target_col+tile)
            if self.current_position(target_row, target_col+tile) != (target_row, target_col+tile):
                print 'Right part tile does not in correct place'
                return False
        conditions +=1
        if conditions == 3:
            print 'All conditions are correct!'
            return True


    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        whole_move = ''
        # replace with your code
        if self._grid[target_row][target_col] != 0:
            # print "DEBUG CASE WHEN ZERO IN JOPA"
            
            # print self
            # print 'Solwing tile', self._grid[target_row][target_col]
            
            # print 'Searchind indexes of ZERO'
            for row in self._grid:
                for col in row:
                    if col == 0:
                        zero_row, zero_col = self._grid.index(row), row.index(col)
                        break
            # print 'ZERO indexes=', (zero_row, zero_col)
            #####Moving zero to correct place
            #path_down = (target_row - zero_row) * 'd'
            #path_left  = (zero_col - target_col) * 'l'
            if target_col - zero_col > 0:
                #path_right = (target_col - zero_col) * 'r'
                path_of_zero =   (zero_col - target_col) * 'l' + (target_row - zero_row) * 'd' + (target_col - zero_col) * 'r'
            else:
                path_of_zero =   (zero_col - target_col) * 'l' + (target_row - zero_row) * 'd'
            zero_col -= len(filter(lambda x: x=='l', path_of_zero))
            zero_col += len(filter(lambda x: x=='r', path_of_zero))
            zero_row += len(filter(lambda x: x=='d', path_of_zero))
            self.update_puzzle(path_of_zero)
            # print 'Grid after moving ZERO to target spot'
            # print self
            whole_move += path_of_zero
        assert self.lower_row_invariant(target_row, target_col), "Invarian is False"
        
        #current_position = self.current_position(target_row, target_col)
        #current_row, current_col = self.current_position(target_row, target_col)
        # print 'Target tile position=',current_position
        # print 'Target tile value=', self._grid[current_position[0]][current_position[1]]
        # print '0 position=', (target_row, target_col)
        
        ######Moving zero tile to the target tile
        path_up = (target_row - self.current_position(target_row, target_col)[0]) * 'u'
        zero_row = target_row - len(path_up)
        if target_col < self.current_position(target_row, target_col)[1]: # Right move
            path_side  = (self.current_position(target_row, target_col)[1] - target_col) * 'r'
            zero_col =  target_col + len(path_side)
        else: # Left move
            path_side =  (target_col - self.current_position(target_row, target_col)[1]) * 'l'
            zero_col =  target_col - len(path_side)
        
        #path_for_zero = path_up + path_side
        # print '------------------------------------------'
        # print 'Move to ZERO =', path_for_zero
        
        self.update_puzzle(path_up + path_side)
        
        # print 'Grid after move:'
        # print self
        # current_position = self.current_position(target_row, target_col)        
        # current_row, current_col = current_position
        # print 'Updated Target tile position=',current_position
        # print 'Updated 0 position=', (zero_row, zero_col)
        # print 'Target position =', (target_row, target_col)
        # print '-----------------------------------------'
        

        ###### New moves after moving ZERO tile into target tile
        # counter = 0
        whole_move += path_up + path_side
        while  self.current_position(target_row, target_col) != \
                (target_row, target_col) or zero_col != target_col - 1:
            # tt_in_home = self.current_position(target_row, target_col) == \
            #     (target_row, target_col)

            cyclic_moves = ''
            # counter += 1
            #current_position = self.current_position(target_row, target_col)        
            #current_col = self.current_position(target_row, target_col)[1]
            # print 'Zero coloumn', zero_col, '== Target coloumn', target_col
            # print zero_col == target_col 
            
            #### Case 1 if ZERO located in ther right of
            #### target tile (after it)
            if zero_col > self.current_position(target_row, target_col)[1]:
                # print ' Look in the up puzzle, zero on the right side'
                # if self.current_position(target_row, target_col)[1] != target_col:
                #     # print 'not under target place'
                #     cyclic_moves = 'dllur'
                #     zero_col -= len(filter(lambda x: x=='l', cyclic_moves))
                #     zero_col += len(filter(lambda x: x=='r', cyclic_moves))
                if self.current_position(target_row, target_col)[1] == target_col and self._grid[zero_row+1][zero_col] < \
                                                    self._grid[self.current_position(target_row, target_col)[0]][self.current_position(target_row, target_col)[1]]:
                    # print 'Tile tat is under ZERO is',self._grid[zero_row+1][zero_col] 
                    # print 'TT under target place'
                    cyclic_moves = 'dlu'
                    zero_col -= len(filter(lambda x: x=='l', cyclic_moves))
                    #zero_col += len(filter(lambda x: x=='r', cyclic_moves))
                # elif self._grid[zero_row+1][zero_col] > \
                #     self._grid[self.current_position(target_row, target_col)[0]][self.current_position(target_row, target_col)[1]]:
                #     # print 'Tile under zero is illegal to move and we use upper cycle move '
                        
                #     cyclic_moves = 'ul'
                #     zero_col -= len(filter(lambda x: x=='l', cyclic_moves))
                #     zero_col += len(filter(lambda x: x=='r', cyclic_moves))

            #### Case 2 if ZERO located under the target tile, and both
            #### of them located under the target position of the target tile
            elif zero_col == self.current_position(target_row, target_col)[1] and zero_col == target_col:
                # print 'Both under the target place'
                # print 'TT in home=', tt_in_home
                if self.current_position(target_row, target_col) == \
                (target_row, target_col):
                    cyclic_moves = 'ld'
                    zero_col -= len(filter(lambda x: x=='l', cyclic_moves))
                    #zero_col += len(filter(lambda x: x=='r', cyclic_moves))
                
                else:
                    cyclic_moves = 'lddru'
                    zero_col -= len(filter(lambda x: x=='l', cyclic_moves))
                    zero_col += len(filter(lambda x: x=='r', cyclic_moves))
            
            #### Case 3 if ZERO located in the left side of the target tile
            ### like in the owel-test case
            elif zero_col < self.current_position(target_row, target_col)[1]:
                # print 'ZERO tile located in the left side'
                if self.current_position(target_row, target_col)[1] != target_col:
                    # print 'not under the target place'
                    cyclic_moves = 'drrul'
                    zero_col -= len(filter(lambda x: x=='l', cyclic_moves))
                    zero_col += len(filter(lambda x: x=='r', cyclic_moves))
                elif self.current_position(target_row, target_col)[1] == target_col:
                    # print 'Target tile under target place'
                    cyclic_moves = 'dru'
                    #zero_col -= len(filter(lambda x: x=='l', cyclic_moves))
                    zero_col += len(filter(lambda x: x=='r', cyclic_moves))


            # print 'Puzzle after Maded move:', cyclic_moves
            self.update_puzzle(cyclic_moves)
            # print 'Zero at home=', 'Zero col', zero_col, '== Target col - 1 is', target_col - 1
            # print self
            # print 'Loot counter =',counter
            whole_move += cyclic_moves
            # if counter > 12:
                # break
        # print 'Tile is solved with move '+ whole_move
        assert self.lower_row_invariant(target_row, target_col-1), "Invarian is False"
        return whole_move
         


        

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # print '----------------------------------'
        # print 'SOLVING ZERO COLOUMN'
        assert self.lower_row_invariant(target_row,0), "Invarian is False"
        whole_move = ''
        #current_position = self.current_position(target_row, 0)
        current_row, current_col = self.current_position(target_row, 0)
        zero_row, zero_col = target_row, 0
        # print 'Target tile position=',current_position
        # print 'Target tile value=', self._grid[current_position[0]][current_position[1]]
        # print '0 position=', (target_row, 0)
        # print '------------------------------------------'
        # print 'Recommended move ur'
        
        recomended_move = 'ur'
        whole_move += recomended_move
        zero_col += len(filter(lambda x: x=='r', recomended_move))
        zero_row -= len(filter(lambda x: x=='u', recomended_move))
        self.update_puzzle(recomended_move)
        # print 'Grid after move:', recomended_move
        # print self
        # print 'Updated Target tile position=',self.current_position(target_row, 0)
        # print 'Updated 0 position=', (zero_row, zero_col)
        # print 'Target position =', (target_row, 0)
        current_position = self.current_position(target_row, 0)
        current_row, current_col = current_position
        if self.current_position(target_row, 0) == \
                (target_row, 0):
                # print 'TT stays in correct place after recomended move'
                zero_to_place_move = 'r' * (self._width-1 - zero_col)
                self.update_puzzle(zero_to_place_move)
                whole_move += zero_to_place_move
                # print self
                assert self.lower_row_invariant(target_row-1,self._width-1), "Invarian is False"
                return whole_move
            #move ZERO tile to the right
        else:
            # print '------------------------------'
            # print 'After base move we are do not finde puzzle'
            # print 'Lets move zero towards TT'
            ### reposition TT to (target_row -1, 1)
            ### reposition ZERO tile to (target_row-1,0)
    
        ######Moving zero tile to the target tile
            #path_up = (zero_row - current_row) * 'u'
            #path_side  = (current_col - zero_col) * 'r'
            path_for_zero =  (zero_row - current_row) * 'u' + (current_col - zero_col) * 'r'
            whole_move += path_for_zero
            zero_col += len(filter(lambda x: x=='r', path_for_zero))
            zero_row -= len(filter(lambda x: x=='u', path_for_zero))
            self.update_puzzle(path_for_zero)
            # print 'grid after move', path_for_zero
            # print self
            # print 'Updated Target tile position=',self.current_position(target_row, 0)
            # print 'Updated 0 position=', (zero_row, zero_col)
            # print 'Target position =', (target_row, 0)
            counter = 0
            while self.current_position(target_row, 0) != (target_row -1, 1) or \
                    (zero_row,zero_col) != (target_row-1,0):
                cyclic_moves = ''
                current_position = self.current_position(target_row, 0)
                current_row, current_col = current_position
                # print 'We are in while loop'
                counter += 1
                if zero_row < current_row:
                    # print 'Zero row under current TT '
                    if self.current_position(target_row, 0) == (target_row -1, 1):
                        # print 'TT is in the reccomended posiont (target_row -1, 1) \n and we are movind zero to the left side of TT '
                        cyclic_moves = 'ld'
                        whole_move += cyclic_moves
                        zero_col -= len(filter(lambda x: x=='l', cyclic_moves))
                        zero_row += len(filter(lambda x: x=='d', cyclic_moves))
                    else:
                        # print 'TT should be one tile down'
                        cyclic_moves = 'lddru'
                        whole_move += cyclic_moves
                        zero_col -= len(filter(lambda x: x=='l', cyclic_moves))
                        zero_col += len(filter(lambda x: x=='r', cyclic_moves))
                        zero_row += len(filter(lambda x: x=='d', cyclic_moves))
                        zero_row -= len(filter(lambda x: x=='u', cyclic_moves))
                #### Case 1 if ZERO located in the right of
                #### target tile (after it)
                if zero_col > current_col:
                    # print ' Look in the up puzzle, zero in the right side'
                    if current_col != 1:
                        # print 'not under target place (target_row -1, 1)'
                        cyclic_moves = 'dllur'
                        zero_col -= len(filter(lambda x: x=='l', cyclic_moves))
                        zero_col += len(filter(lambda x: x=='r', cyclic_moves))
                        whole_move += cyclic_moves
                    # elif current_col == 1 and self._grid[zero_row+1][zero_col] < \
                    #                                     self._grid[current_position[0]][current_position[1]]:
                    elif current_col == 1:    
                        # print 'Tile tat is under ZERO is',self._grid[zero_row+1][zero_col] 
                        # print 'TT under target place'
                        cyclic_moves = 'dlu'
                        whole_move += cyclic_moves
                        zero_col -= len(filter(lambda x: x=='l', cyclic_moves))
                        zero_col += len(filter(lambda x: x=='r', cyclic_moves))
                    elif self._grid[zero_row+1][zero_col] > \
                        self._grid[current_position[0]][current_position[1]]:
                        print 'Tile under zero is illegal to move and we use upper cycle move '
                            
                        cyclic_moves = 'ul'
                        zero_col -= len(filter(lambda x: x=='l', cyclic_moves))
                        zero_col += len(filter(lambda x: x=='r', cyclic_moves))
                # print 'Puzzle after Maded move:', cyclic_moves
                self.update_puzzle(cyclic_moves)
                # print 'Zero at home=', 'Zero col', zero_col, '== Target col - 1 is', target_col - 1
                # print self
                # print 'Loop counter =',counter
                if counter > 10:
                    break
        ### Solwing 3x2 puzzle
        # print '--------------------------'
        # print 'Lets solve 3x2 puzzle formed recently'
        move3x2 = 'ruldrdlurdluurddlur'
        whole_move += move3x2
        zero_col -= len(filter(lambda x: x=='l', move3x2))
        zero_col += len(filter(lambda x: x=='r', move3x2))
        zero_row += len(filter(lambda x: x=='d', move3x2))
        zero_row -= len(filter(lambda x: x=='u', move3x2))
        self.update_puzzle(move3x2)
        # print 'Grid afret 3x2 solver move'
        # print self
        # print 'Updated Target tile position=',self.current_position(target_row, 0)
        # print 'Updated 0 position=', (zero_row, zero_col)
        # print 'Target position =', (target_row, 0)
        #####Moving ZERO to the (target_row - 1, n - 1) position where
        ##### 'n' is a grid height.
        # print self._width-1 - zero_col
        zero_to_place_move = 'r' * (self._width-1 - zero_col)
        whole_move += zero_to_place_move
        self.update_puzzle(zero_to_place_move)
        # print self
        assert self.lower_row_invariant(target_row-1,self._width-1), "Invarian is False"
        return whole_move

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        conditions = 0
        current = self._grid[0][target_col] == 0
        if current:
            conditions +=1
        else:
            # print 'Tile ZERO is not at (0, %s) position' %(target_col)
            return False
        
        below_row = 1 + 1
        for _ in range(1, self._height - below_row):
            below_row += 1
            for ind in range(len(self._grid[below_row])):
                if self.current_position(below_row, ind) != (below_row, ind):
                    # print 'Some tile in the lower row does not in correct place in row0_invariant' 
                    return False
        conditions += 1
        

        for ind in range(len(self._grid[1][target_col:])):
            if self.current_position(1, ind+target_col) != (1, ind+target_col):
                # print 'Some tile in the lower row does not in correct place in row0_invariant' 
                return False
        conditions += 1
        if conditions == 3:
            # print 'All conditions are cprrect!'
            return True
        

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        conditions = 0
        current = self._grid[1][target_col] == 0
        if current:
            conditions +=1
        else:
            # print 'Tile ZERO is not at (0, %s) position' %(target_col)
            return False
        
        below_row = 1 + 1
        for _ in range(1, self._height - below_row):
            below_row += 1
            for ind in range(len(self._grid[below_row])):
                if self.current_position(below_row, ind) != (below_row, ind):
                    # print 'Some tile in the lower row does not in correct place in row1_invariant' 
                    return False
        conditions += 1
        if conditions == 2:
            # print 'All conditions are correct!'
            return True
        

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        assert self.row0_invariant(target_col), 'Some trouble in row0_invariant' 
        whole_move = ''
        #current_position = self.current_position(0, target_col)
        current_row, current_col = self.current_position(0, target_col)
        # print self.get_number(current_row, current_col)
        zero_row, zero_col = 0, target_col
        # print 'Target tile position=',self.current_position(0, target_col)
        # print 'Target tile value=', self._grid[current_position[0]][current_position[1]]
        # print '0 position=', (0, target_col)
        # print '------------------------------------------'
        # print 'Recommended move ld'
        
        recomended_move = 'ld'
        whole_move += recomended_move
        zero_col -= len(filter(lambda x: x=='l', recomended_move))
        zero_row += len(filter(lambda x: x=='d', recomended_move))
        self.update_puzzle(recomended_move)
        # print 'Grid after move:', recomended_move
        # print self
        # print 'Updated Target tile position=',self.current_position(0, target_col)
        # print 'Updated 0 position=', (zero_row, zero_col)
        # print 'Target position =', (0, target_col)
        #####Case when we check if recomended move solves the tile
        if self.current_position(0, target_col) == (0, target_col):
            # print 'Congrads recomended move made great deal !!'
            return whole_move
        #####If not, we position TT to (1, target_col-1),
        ##### and ZEOR to (1, target_col-2)
        else:
            # print '------------------------------'
            # print 'After base move we are do not finde puzzle'
            # print 'Lets move zero towards TT'
    
        ######Moving zero tile to the target tile
            path_up = (zero_row - current_row) * 'u'
            path_side  = (zero_col - current_col) * 'l'
            path_for_zero =  path_up + path_side
            whole_move += path_for_zero
            zero_col -= len(filter(lambda x: x=='l', path_for_zero))
            zero_row -= len(filter(lambda x: x=='u', path_for_zero))
            self.update_puzzle(path_for_zero)
            
            # print 'grid after move', path_for_zero
            # print self
            # print 'Updated Target tile position=',self.current_position(0, target_col)
            # print 'Updated 0 position=', (zero_row, zero_col)
            # print 'Target position =', (0, target_col)
            counter = 0
            # print  self.current_position(0, target_col) != (1, target_col-1)
            # print (zero_row,zero_col) != (1,target_col-2)
            ####POitioning TT and zero into positions that can be solvable
            while self.current_position(0, target_col) != (1, target_col-1) or \
                (zero_row,zero_col) != (1,target_col-2):
                counter +=1
                #current_position = self.current_position(0, target_col)
                current_row, current_col = self.current_position(0, target_col)
                cyclic_moves = ''
                # print 'Aloha in the loop'
                if zero_col < current_col:
                    # print 'ZERO tile located in the left side and down move IS  NOT POSIBLE'
                    

                    if current_col != target_col-1 and zero_row == 0:
                        # print 'In the upper row and we can use down cycling'
                        cyclic_moves = 'drrul'
                        whole_move += cyclic_moves
                        zero_col -= len(filter(lambda x: x=='l', cyclic_moves))
                        zero_col += len(filter(lambda x: x=='r', cyclic_moves))
                        zero_row += len(filter(lambda x: x=='d', cyclic_moves))
                        zero_row -= len(filter(lambda x: x=='u', cyclic_moves))

                    elif current_col != target_col-1:
                        # print 'not under the target place'
                        cyclic_moves = 'urrdl'
                        whole_move += cyclic_moves
                        zero_col -= len(filter(lambda x: x=='l', cyclic_moves))
                        zero_col += len(filter(lambda x: x=='r', cyclic_moves))
                        zero_row += len(filter(lambda x: x=='d', cyclic_moves))
                        zero_row -= len(filter(lambda x: x=='u', cyclic_moves))
                    elif current_col == target_col-1:
                        # print 'Target tile under target place'
                        # print 'DEBUG!!!!'
                        # print self
                        # print zero_col, target_col
                        if zero_col == 0 and current_col == 1:
                            cyclic_moves = 'druld'
                        elif zero_row == 0:
                            cyclic_moves = 'druld'
                        
                        else:
                            cyclic_moves = 'urd'
                        whole_move += cyclic_moves
                        zero_row += len(filter(lambda x: x=='d', cyclic_moves))
                        zero_row -= len(filter(lambda x: x=='u', cyclic_moves))
                        zero_col += len(filter(lambda x: x=='r', cyclic_moves))
                        zero_col -= len(filter(lambda x: x=='l', cyclic_moves))
                elif zero_row > current_row:
                    # print 'DEBUG'
                    # print 'TT under zero tile'
                    cyclic_moves = 'uld'
                    whole_move += cyclic_moves
                    zero_row += len(filter(lambda x: x=='d', cyclic_moves))
                    zero_row -= len(filter(lambda x: x=='u', cyclic_moves))
                    zero_col -= len(filter(lambda x: x=='l', cyclic_moves))
                # print 'Puzzle after Maded move:', cyclic_moves
                self.update_puzzle(cyclic_moves)
                # print 'Zero at home=', 'Zero col', zero_col, '== Target col - 1 is', target_col - 1
                # print self
                # print 'Loop counter =',counter
             
                if counter > 10:
                    # print 'COUNTER break'
                    break

        #####Solving using pattern  2 x 3 puzzle
        # print '--------------------------'
        # print 'Lets solve 2x3 puzzle formed recently'
        move2x3 = "urdlurrdluldrruld"
        whole_move += move2x3
        zero_col -= len(filter(lambda x: x=='l', move2x3))
        zero_col += len(filter(lambda x: x=='r', move2x3))
        zero_row += len(filter(lambda x: x=='d', move2x3))
        zero_row -= len(filter(lambda x: x=='u', move2x3))
        self.update_puzzle(move2x3)
        # print self
        assert self.row1_invariant(target_col-1), 'Some trouble in row1_invariant' 
        return whole_move

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        whole_move = ''
        if self._grid[1][target_col] != 0:
            # print "DEBUG CASE WHEN ZERO IN JOPA solve_row1_tile "
            
            # print self
            # print 'Solwing tile', self._grid[1][target_col]
            
            # print 'Searchind indexes of ZERO'
            for row in self._grid:
                for col in row:
                    if col == 0:
                        zero_row, zero_col = self._grid.index(row), row.index(col)
                        break
            # print 'ZERO indexes=', (zero_row, zero_col)
            #####Moving zero to correct place
            #path_down = (1 - zero_row) * 'd'
            # path_left  = (zero_col - target_col) * 'l'
            if target_col - zero_col > 0:
                #path_right = (target_col - zero_col) * 'r'
                path_of_zero =   (1 - zero_row) * 'd' + (target_col - zero_col) * 'r'
            else:
                path_of_zero =   (1 - zero_row) * 'd'
            #zero_col -= len(filter(lambda x: x=='l', path_of_zero))
            #zero_row -= len(filter(lambda x: x=='u', path_of_zero))
            zero_col += len(filter(lambda x: x=='r', path_of_zero))
            zero_row += len(filter(lambda x: x=='d', path_of_zero))
            self.update_puzzle(path_of_zero)
            # print 'Grid after moving ZERO to target spot'
            # print self
            whole_move += path_of_zero

        assert self.row1_invariant(target_col), 'Some trouble in row1_invariant' 
        
        #current_row, current_col = self.current_position(1, target_col)
        zero_row, zero_col = 1, target_col
        ######Moving zero tile to the target tile
        #path_up = (zero_row - current_row) * 'u'
        #path_side  = (zero_col - current_col) * 'l'
        path_for_zero =  (zero_row - self.current_position(1, target_col)[0]) * 'u' + (zero_col - self.current_position(1, target_col)[1]) * 'l'
        whole_move += path_for_zero
        zero_col -= len(filter(lambda x: x=='l', path_for_zero))
        zero_row -= len(filter(lambda x: x=='u', path_for_zero))
        self.update_puzzle(path_for_zero)
        # print 'grid after move', path_for_zero
        # print self
        # print 'Updated Target tile position=',self.current_position(1, target_col)
        # print 'Updated 0 position=', (zero_row, zero_col)
        # print 'Target position =', (1, target_col)
        counter = 0
        while self.current_position(1, target_col) != \
                (1, target_col) or (zero_row, zero_col) != (0, target_col):
            # print 'Welcome to while loop!'
            cyclic_moves = ''
            #### Case 3 if ZERO located in the left side of the target tile
            ### like in the owel-test case
            #current_position = self.current_position(1, target_col)
            current_col = self.current_position(1, target_col)[1]
            counter +=1
            if self.current_position(1, target_col) == \
                (1, target_col):
                # print 'ZERO not under TT'
                cyclic_moves = 'ur'
                whole_move += cyclic_moves
                zero_row -= len(filter(lambda x: x=='u', cyclic_moves))
                zero_col += len(filter(lambda x: x=='r', cyclic_moves))
            elif zero_col < current_col and self._grid[zero_row+1][zero_col] < \
                             self._grid[self.current_position(1, target_col)[0]][self.current_position(1, target_col)[1]]:
                # print 'ZERO tile located in the left side and down move is POSIBLE'
                if current_col != target_col:
                    # print 'not under the target place'
                    cyclic_moves = 'drrul'
                    whole_move += cyclic_moves
                    zero_col -= len(filter(lambda x: x=='l', cyclic_moves))
                    zero_col += len(filter(lambda x: x=='r', cyclic_moves))
                    zero_row += len(filter(lambda x: x=='d', cyclic_moves))
                    zero_row -= len(filter(lambda x: x=='u', cyclic_moves))
                elif current_col == target_col:
                    # print 'Target tile under target place'
                    cyclic_moves = 'dru'
                    whole_move += cyclic_moves
                    zero_row += len(filter(lambda x: x=='d', cyclic_moves))
                    zero_row -= len(filter(lambda x: x=='u', cyclic_moves))
                    zero_col += len(filter(lambda x: x=='r', cyclic_moves))
            elif current_col != target_col and self._grid[zero_row+1][zero_col] > \
                             self._grid[self.current_position(1, target_col)[0]][self.current_position(1, target_col)[1]]:
                    # print 'not under the target place'
                    cyclic_moves = 'urrdl'
                    whole_move += cyclic_moves
                    zero_col -= len(filter(lambda x: x=='l', cyclic_moves))
                    zero_col += len(filter(lambda x: x=='r', cyclic_moves))
                    zero_row += len(filter(lambda x: x=='d', cyclic_moves))
                    zero_row -= len(filter(lambda x: x=='u', cyclic_moves))            









            # elif zero_col < current_col and self._grid[zero_row+1][zero_col] > \
            #                  self._grid[current_position[0]][current_position[1]]:
            #     # print 'ZERO tile located in the left side and down move IS  NOT POSIBLE'
            #     if current_col != target_col:
            #         # print 'not under the target place'
            #         cyclic_moves = 'urrdl'
            #         whole_move += cyclic_moves
            #         zero_col -= len(filter(lambda x: x=='l', cyclic_moves))
            #         zero_col += len(filter(lambda x: x=='r', cyclic_moves))
            #         zero_row += len(filter(lambda x: x=='d', cyclic_moves))
            #         zero_row -= len(filter(lambda x: x=='u', cyclic_moves))
                # elif current_col == target_col:
                #     # print 'Target tile under target place'
                #     cyclic_moves = 'urd'
                #     whole_move += cyclic_moves
                #     zero_row += len(filter(lambda x: x=='d', cyclic_moves))
                #     zero_row -= len(filter(lambda x: x=='u', cyclic_moves))
                #     zero_col += len(filter(lambda x: x=='r', cyclic_moves))

            #cyclic_moves +='ur'
            # print 'Puzzle after Maded move:', cyclic_moves
            self.update_puzzle(cyclic_moves)
            # print 'Zero at home=', 'Zero col', zero_col, '== Target col - 1 is', target_col - 1
            # print self
            # print 'Loop counter =',counter
            if counter > 10:
                break
        return whole_move

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        assert self.row1_invariant(1), '2x2 Dont pass row1_invariant(1)'
        whole_move = ''
        current_position = self.current_position(0, 0)
        # print 'Zero position =', current_position
        counter = 0
        

        
        # if current_position == (0,0):
            # print (0,0)
        #     move_to_00 = 'rdlu' 
        if current_position == (0,1):
            # print (0,1)
            move_to_00 = 'l'
        if current_position == (1,0):
            # print (1,0)
            move_to_00 = 'u'
        if current_position == (1,1):
            # print (1,1)
            move_to_00 = 'ul'
        whole_move += move_to_00
        self.update_puzzle(move_to_00)
        # print self
        # print self.get_number(1,1) < self.get_number(1,0)
        
        while self.get_number(0,0) != 0 or  self.get_number(0,1) != 1:
                
            # print 'Aloha in loop!'
            counter +=1
            move = 'rdlu'
            whole_move += move
            self.update_puzzle(move)
            # print self
            if counter >5:
                break
        return whole_move
    
    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        
        counter = 0
        rows = self._height-1
        cols = self._width-1
        # print rows, cols
        # print 'The greed has %s rows and %s coloumn indexes' %(rows, cols) 
        solution_move = ''
        if self.get_number(0,0) == 0 and \
            self.get_number(0,1) == 1:
            # print 'Congrads Puxxle is Aolved at start!!!!!'
            return ''
        #appropriate_number = (self._height * self._width) - 1
        appropriate_number = (rows+1) * (cols+1) -1
        # print 'First appropriate_number=',appropriate_number
        # print "Grid first tile that we will solwing has value =", self._grid[rows][cols]
        
        while counter < 300:
            counter +=1
            # print self
            #appropriate_number = (rows+1) * (cols+1) -1
            # print 'Appropriate number in loop=',appropriate_number
            # print 'We are solving %s index_row and %s index_col' %(rows, cols) 
            ####Case when we use solve_interior_tile
            if rows > 1 and cols > 0:
                if self._grid[rows][cols] == appropriate_number:
                    # print 'This tile is already solved!!!'
                    cols -= 1
                    appropriate_number -=1
                else:
                    # print 'We are solving interior tile', (rows, cols)
                    solution_move += self.solve_interior_tile(rows, cols)
                    # print 'Solution move=', solution_move
                    cols -= 1
            #### Case when we use solve_col0_tile
            elif rows > 1 and cols == 0:
                if self._grid[rows][cols] == appropriate_number:
                    # print 'This tile is already solved!!!'
                    rows -= 1
                    cols = self._width-1
                    appropriate_number -=1
                else:
                    # print 'We are solwing tile 0 in row', rows
                    # print 'Appropriate number here ='
                    solution_move += self.solve_col0_tile(rows)
                    # print 'Solution move=', solution_move
                    rows -=1
                    cols = self._width-1


            #### Cases when we use solve_row0_tile
            elif rows == 1 and cols > 1:
                if self._grid[rows][cols] == appropriate_number:
                    # print 'This tile is already solved!!!'
                    rows -= 1
                    #cols = self._width-1
                    appropriate_number -= self._width

                else:
                    # print 'Solving upper 2 rows right side'
                    solution_move += self.solve_row1_tile(cols)
                    rows -=1
                    appropriate_number -= self._width
             #### Cases when we use solve_row1_tile    
            if rows < 1 and cols > 1:
                if self._grid[rows][cols] == appropriate_number:
                    # print 'This tile is already solved!!!'
                    rows += 1
                    cols -= 1
                    appropriate_number +=self._width-1
                else:
                    # print '(1,J) tile solved, lets solwe tile (0,j) in tile',(rows,cols)
                    # print 'Greed after move solve_row1_tile'
                    # print self
                    solution_move += self.solve_row0_tile(cols)
                    rows +=1
                    cols -=1
                    appropriate_number +=self._width-1


            #### Case when we use solve_2x2
            elif rows <= 1 and cols <= 1:
                # print 'We are solving 2x2 puzzle'
                solution_move += self.solve_2x2()
                if self._grid[0][0] == 0 and \
                   self._grid[0][1] == 1:
                   # print 'Congrads Puxxle is SOLVED!!!!!'
                   break




            if counter > 100:
                # print 'COUNTER BREAK'
                break
        # print solution_move, len(solution_move)
        return solution_move






        # for row in solution_greed._grid[::-1]:
            # print solution_greed._grid
            # print 'Row =',row
            
        #     if solution_greed._grid.index(row) > 1:
                # print "Case when we solwing Interior and Tile0 part"
                

        #         for col in solution_greed._grid[solution_greed._grid.index(row)][::-1]:
                    # print 'Coloumn value=', col
                    #print row[0]
        #             if col !=row[0]:
                        # print 'Case when we use just Interior tile solution'
                        # print solution_greed._grid.index(row)
                        # print row.index(col)
    
        #                 solution += solution_greed.solve_interior_tile(solution_greed._grid.index(row) , row.index(col))
                        # print 'Solution =', solution
                        # print self 
                        # print solution_greed._grid
        #             elif col ==row[0]:
                        # print 'Case when we use just Col0 solution'

        #     else:
                # print 'Case when we solwing first two rows'

        #return ""

### Start interactive simulation

poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
# puzzle = Puzzle(4,4)

###Solver case1
# puzzle.update_puzzle('dddr')
# puzzle.set_number(0,3,13)
# puzzle.set_number(3,0,2)
# print puzzle
# puzzle.solve_interior_tile(3,1)
# puzzle.solve_col0_tile(3)

###Case 2
# puzzle.update_puzzle('ddrr')
# puzzle.set_number(1,3,10)
# puzzle.set_number(2,1,7)
# print puzzle
# puzzle.solve_interior_tile(2,2)
# puzzle.solve_interior_tile(2,1)
# puzzle.set_number(0,3,8)
# puzzle.set_number(1,0,2)
# puzzle.solve_col0_tile(2)

###Case 3
#puzzle.update_puzzle('ddrr')
#puzzle.set_number(0,0,10)
#puzzle.set_number(2,0,2)

###Owl test case
# owl_puzzle = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
# print owl_puzzle
# owl_puzzle.solve_interior_tile(2,2)
# print puzzle

# owl_puzzle = Puzzle(4, 5, [[12, 11, 10, 9, 15], [7, 6, 5, 4, 3], [2, 1, 8, 13, 14], [0, 16, 17, 18, 19]])
# print owl_puzzle
# owl_puzzle.solve_col0_tile(3)

# owl_puzzle =  Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
# print owl_puzzle
# print owl_puzzle.row0_invariant(2)

# owl_puzzle_1 = Puzzle(4, 5, [[15, 6, 5, 3, 4], [2, 1, 0, 8, 9], [10, 11, 12, 13, 14], [7, 16, 17, 18, 19]])
# print owl_puzzle_1
# print owl_puzzle_1.row1_invariant(2) 

# owl_puzzle = Puzzle(4, 5, [[7, 6, 5, 3, 2], [4, 1, 9, 8, 0], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
# print owl_puzzle
# print owl_puzzle.solve_row1_tile(4)

# owl_puzzle_1 = Puzzle(3, 3, [[2, 5, 4], [1, 3, 0], [6, 7, 8]])
# print owl_puzzle_1
# print owl_puzzle_1.solve_row1_tile(2)

# owl_puzzle = Puzzle(3, 3, [[4, 1, 0], [2, 3, 5], [6, 7, 8]])
# print owl_puzzle
# print owl_puzzle.solve_row0_tile(2)


# owl_puzzle_1 =  Puzzle(4, 5, [[7, 6, 5, 3, 0], [4, 8, 2, 1, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
# print owl_puzzle_1
# print owl_puzzle_1.solve_row0_tile(4)

# owl_puzzle = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]])
# print owl_puzzle
# print owl_puzzle.solve_2x2()

# owl_puzzle = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
# print owl_puzzle
# print owl_puzzle.solve_puzzle()


# owl_puzzle =Puzzle(2, 4, [[0, 3, 2, 7], [4, 5, 6, 1]])
# print owl_puzzle
# print owl_puzzle.solve_puzzle()
