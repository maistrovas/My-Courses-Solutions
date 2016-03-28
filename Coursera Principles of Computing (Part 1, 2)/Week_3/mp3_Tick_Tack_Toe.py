"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 10         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player 
# PlayerX
SCORE_OTHER = 1.0   # Score for squares played by the other player
#PlayerO

def mc_trial(board, player):
    '''
    Simulate entire game
    '''
    states = [provided.PLAYERX, provided.PLAYERO, provided.DRAW, provided.EMPTY]
    while board.check_win() == None:
        r_cel = random.choice(board.get_empty_squares())
        board.move(r_cel[0],r_cel[1], player)
        state = board.check_win()
        if state in states:
            break
        r_cel = random.choice(board.get_empty_squares())
        board.move(r_cel[0],r_cel[1], provided.switch_player(player))
        state = board.check_win()
        if state in states:
            break

def mc_update_scores(scores, board, player):
    '''
    Upadate scores after game simulation '+' points for viner
    and '-' for luser
    '''
    if board.check_win() == player:
                        #machine, PLAYERX, Score = SCORE_CURRENT
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.square(row,col) == player:
                    scores[row][col] += SCORE_CURRENT
                if board.square(row,col) == provided.switch_player(player):
                    scores[row][col] -= SCORE_OTHER
    if board.check_win() == provided.switch_player(player): 
                        #Human, playerO, Score = SCORE_OTHER
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.square(row,col) == player:
                    scores[row][col] -= SCORE_CURRENT
                if board.square(row,col) == provided.switch_player(player):
                    scores[row][col] += SCORE_OTHER
        
def get_best_move(board, scores):
    '''
    Analuzes results bumber of sumulated games and
    defines the best future muve 
    '''
    list_scores = {}
    for square in board.get_empty_squares():
        list_scores[square] = scores[square[0]][square[1]]
    maxx = max(list_scores.values()) 
    variants = []
    for square in list_scores:
        if list_scores[square] == maxx:
            variants.append(square)
    return random.choice(variants)

def mc_move(board, player, trials):
    '''
    Uses the above simulations to determine 
    vich move would be most efficient.
    '''
    scores = [[0 for _ in range(board.get_dim())]
             for _ in range(board.get_dim())]
    curent_board = board.clone()
    for _ in range(trials):
        curent_board = board.clone()
        mc_trial(curent_board, player)
        mc_update_scores(scores, curent_board, player )
    machine_move = get_best_move(board, scores)  
    return machine_move
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
