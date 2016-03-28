"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
#import codeskulptor
#codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def make_full(board,player):
    '''
    Partially full the board to minimize recursion process
    '''
    squares = board.get_empty_squares()
    half_total = len(squares) / 3
    counter = 0
    for poss_move in board.get_empty_squares():
        player = provided.switch_player(player)
        board.move(poss_move[0], poss_move[1], player)
        counter += 1
        if counter == half_total:
            break
    return board

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    #Base case
    if board.check_win() != None:
        return SCORES[board.check_win()], (-1,-1)
    # worst values
    results = (-1, (-1,-1))
    scores = []
    for poss_move in board.get_empty_squares():
        new_board = board.clone()
        new_board.move(poss_move[0], poss_move[1], player)
        score, dummy_move = mm_move(new_board, provided.switch_player(player))
        scores.append((score, poss_move))
        if score * SCORES[player] == 1:
            return (score, poss_move)
        elif score * SCORES[player] == 0:
            results = (score, poss_move)
        elif results[0] == -1:
            results = (results[0], poss_move)
    return results[0] * SCORES[player], results[1]

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    # make_full(board,player)
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
